#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This is the render object for the search interface."""
from collections import OrderedDict
from six import text_type
import requests
from .config import get_config
from .admin import AdminPolicy

ELASTIC_INDEX = get_config().get('elasticsearch', 'index')
CACHE_SIZE = get_config().getint('policy', 'cache_size')
RELEASER_UUID = AdminPolicy().get_relationship_info(name='authorized_releaser')[0].get('uuid')
SEARCH_REQUIRED_UUID = AdminPolicy().get_relationship_info(name='search_required')[0].get('uuid')


class LimitedSizeDict(OrderedDict):
    """Limited caching dictionary."""

    def __init__(self, *args, **kwds):
        """Constructor for caching dictionary."""
        self.size_limit = kwds.pop('size_limit', None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __getitem__(self, key):
        """Get the item and put it back so it's on top."""
        val = OrderedDict.__getitem__(self, key)
        try:
            del self[key]
            OrderedDict.__setitem__(self, key, val)
        except KeyError:  # pragma: no cover can't get this covered
            # the key must have gotten purged...
            pass
        return val

    # pylint: disable=signature-differs
    def __setitem__(self, key, value):
        """Set item foo[key] = value."""
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()
    # pylint: enable=signature-differs

    def _check_size_limit(self):
        """Function to set the item and remove old ones."""
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)


def transsip_transsap_render(trans_obj, render_func, obj_cls, trans_key):
    """Wrapper method to handle transaction relationships."""
    ret = {}
    for trans_rel in ['transsip', 'transsap']:
        try:
            obj = SearchRender.get_obj_by_id(trans_rel, trans_obj['_id'])
            ret[obj[trans_key]] = render_func(
                SearchRender.get_obj_by_id(obj_cls, obj[trans_key]))
        except IndexError:
            pass
    return [value for _key, value in ret.items()]


def trans_has_doi(trans_obj):
    """Return true if the transaction has a doi otherwise false."""
    trans_doi = SearchRender.get_trans_doi(trans_obj['_id'])
    if trans_doi != 'false':
        return 'true'
    return 'false'


def trans_access_url(trans_obj):
    """Figure out the access url for the transaction."""
    trans_doi = SearchRender.get_trans_doi(trans_obj['_id'])
    if trans_doi != 'false':
        return get_config().get('policy', 'doi_url_format').format(doi=trans_doi)
    if SearchRender.get_trans_release(trans_obj['_id']) == 'true':
        return get_config().get('policy', 'release_url_format').format(transaction=trans_obj['_id'])
    return get_config().get('policy', 'internal_url_format').format(transaction=trans_obj['_id'])


def trans_science_themes(trans_obj):
    """Render the science theme from a project."""
    return transsip_transsap_render(
        trans_obj, SearchRender.render_science_theme,
        'projects', 'project'
    )


def trans_projects(trans_obj):
    """Render the projects for a transaction."""
    return transsip_transsap_render(
        trans_obj, lambda x: SearchRender.render('projects', x),
        'projects', 'project'
    )


def trans_inst_groups(trans_obj):
    """Render the instrument groups for a transaction."""
    try:
        obj = SearchRender.get_obj_by_id('transsip', trans_obj['_id'])
        return SearchRender.get_groups_from_instrument(obj['instrument'])
    except IndexError:
        pass
    return []


def trans_instruments(trans_obj):
    """Render the instruments for a transaction."""
    try:
        obj = SearchRender.get_obj_by_id('transsip', trans_obj['_id'])
        return [
            SearchRender.render(
                'instruments',
                SearchRender.get_obj_by_id('instruments', obj['instrument'])
            )
        ]
    except IndexError:
        pass
    return []


def trans_institutions(trans_obj):
    """Render the institutions for a transaction."""
    ret = []
    for trans_rel in ['transsip', 'transsap']:
        try:
            obj = SearchRender.get_obj_by_id(trans_rel, trans_obj['_id'])
            ret.extend(SearchRender.get_institutions_from_user(
                obj['submitter']))
        except IndexError:
            pass
    return ret


def trans_users(trans_obj):
    """Render the users list for transactions."""
    return transsip_transsap_render(
        trans_obj, lambda x: SearchRender.render('users', x),
        'users', 'submitter'
    )


def instrument_kvp(inst_obj):
    """Generate a list of key value pairs for transaction."""
    return SearchRender.get_instrument_kvp(inst_obj['_id'])


def trans_kvp(trans_obj):
    """Generate a list of key value pairs for transaction."""
    return SearchRender.get_trans_kvp(trans_obj['_id'])


def user_release(obj):
    """Render the transaction release attribute."""
    return SearchRender.get_user_release(obj['_id'])


def proj_release(obj):
    """Render the transaction release attribute."""
    return SearchRender.get_proj_release(obj['_id'])


def trans_release(obj):
    """Render the transaction release attribute."""
    return SearchRender.get_trans_release(obj['_id'])


# pylint: disable=too-many-public-methods
class SearchRender(object):
    """Search render class to contain methods."""

    obj_cache = LimitedSizeDict(size_limit=CACHE_SIZE)
    render_data = {
        'values': {
            'obj_id': text_type('values_{_id}'),
            'value': text_type('{value}'),
            'display_name': text_type('{display_name}'),
            'description': text_type('{description}'),
            'release': text_type('true')
        },
        'keys': {
            'obj_id': text_type('keys_{_id}'),
            'key': text_type('{key}'),
            'display_name': text_type('{display_name}'),
            'description': text_type('{description}'),
            'release': text_type('true')
        },
        'instruments': {
            'obj_id': text_type('instruments_{_id}'),
            'display_name': text_type('{display_name}'),
            'long_name': text_type('{name}'),
            'key_value_pairs': instrument_kvp,
            'keyword': text_type('{display_name}'),
            'release': text_type('true')
        },
        'institutions': {
            'obj_id': text_type('institutions_{_id}'),
            'display_name': text_type('{name}'),
            'keyword': text_type('{name}'),
            'release': text_type('true')
        },
        'users': {
            'obj_id': text_type('users_{_id}'),
            'display_name': text_type('{last_name}, {first_name} {middle_initial}'),
            'keyword': text_type('{last_name}, {first_name} {middle_initial}'),
            'release': user_release
        },
        'projects': {
            'obj_id': text_type('projects_{_id}'),
            'display_name': text_type('{title}'),
            'long_name': text_type(''),
            'abstract': text_type('{abstract}'),
            'title': text_type('{title}'),
            'keyword': text_type('{title}'),
            'release': proj_release,
            'updated_date': text_type('{updated}'),
            'created_date': text_type('{created}'),
            'closed_date': text_type('{closed_date}'),
            'actual_end_date': text_type('{actual_end_date}'),
            'actual_start_date': text_type('{actual_start_date}')
        },
        'groups': {
            'obj_id': text_type('groups_{_id}'),
            'display_name': text_type('{name}'),
            'keyword': text_type('{name}'),
            'release': text_type('true')
        },
        'transactions': {
            'obj_id': text_type('transactions_{_id}'),
            'access_url': trans_access_url,
            'has_doi': trans_has_doi,
            'users': trans_users,
            'institutions': trans_institutions,
            'instruments': trans_instruments,
            'instrument_groups': trans_inst_groups,
            'projects': trans_projects,
            'science_themes': trans_science_themes,
            'release': trans_release,
            'key_value_pairs': trans_kvp,
            'updated_date': text_type('{updated}'),
            'created_date': text_type('{created}')
        }
    }

    global_get_args = {
        'recursion_depth': '0',
        'recursion_limit': '1'
    }

    @classmethod
    def merge_get_args(cls, get_args):
        """Change a hash of get args and global get args into string for url."""
        get_args.update(cls.global_get_args)
        get_list = []
        for key, val in get_args.items():
            get_list.append(text_type('{}={}').format(key, val))
        return '&'.join(get_list)

    @classmethod
    def get_obj_by_id(cls, obj, obj_id):
        """Get the user from metadata and put it in cache."""
        key = text_type('{}_{}').format(obj, obj_id)
        val = cls.obj_cache.get(key, None)
        if val is not None:
            return val
        url = '{base_url}/{obj}?'+cls.merge_get_args({'_id': '{obj_id}'})
        resp = requests.get(
            text_type(url).format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                obj=obj,
                obj_id=obj_id
            )
        )
        cls.obj_cache[key] = resp.json()[0]
        return cls.obj_cache[key]

    @classmethod
    def get_trans_doi(cls, trans_id):
        """Get the transaction doi and return false or doi."""
        resp = requests.get(
            text_type('{base_url}/transaction_user?{args}').format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                args=cls.merge_get_args({'transaction': trans_id, 'relationship': RELEASER_UUID})
            )
        )
        assert resp.status_code == 200
        if not resp.json():
            return 'false'
        rel_uuid = resp.json()[0].get('uuid')
        resp = requests.get(
            text_type('{base_url}/doi_transaction?{args}').format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                args=cls.merge_get_args({'transaction': rel_uuid})
            )
        )
        resp_json = resp.json()
        if resp_json:
            return resp_json[0].get('doi', 'false')
        return 'false'

    @classmethod
    def get_trans_release(cls, trans_id):
        """Get the transaction release and return true/false."""
        resp = requests.get(
            text_type('{base_url}/transaction_user?{args}').format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                args=cls.merge_get_args({'transaction': trans_id, 'relationship': RELEASER_UUID})
            )
        )
        if resp.json():
            return 'true'
        return 'false'

    @classmethod
    def get_instrument_kvp(cls, inst_id):
        """Get the instrument key value pairs."""
        resp = requests.get(
            text_type('{base_url}/instrument_key_value?{args}').format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                args=cls.merge_get_args({'instrument': inst_id, 'relationship': SEARCH_REQUIRED_UUID})
            )
        )
        kvp_hash = {}
        kvp_objs = []
        for kvp_obj in resp.json():
            key_name = cls.get_obj_by_id('keys', kvp_obj.get('key')).get('key')
            value_name = cls.get_obj_by_id('values', kvp_obj.get('value')).get('value')
            kvp_hash[key_name] = value_name
            kvp_objs.append({'key': key_name, 'value': value_name})
        return {
            'key_value_hash': kvp_hash,
            'key_value_objs': kvp_objs
        }

    @classmethod
    def get_trans_kvp(cls, trans_id):
        """Get the transaction key value pairs."""
        resp = requests.get(
            text_type('{base_url}/transactioninfo/by_id/{trans_id}').format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                trans_id=trans_id
            )
        )
        kvp_hash = resp.json().get('key_values', {})
        return {
            'key_value_hash': kvp_hash,
            'key_value_objs': [{'key': key, 'value': value} for key, value in kvp_hash.items()]
        }

    @classmethod
    def get_proj_release(cls, proj_id):
        """Get the project release from transactions on that proj."""
        for trans_rel in ['transsip', 'transsap']:
            resp = requests.get(
                text_type('{base_url}/{trans_rel}?{args}').format(
                    trans_rel=trans_rel,
                    base_url=get_config().get('metadata', 'endpoint_url'),
                    args=cls.merge_get_args({'project': proj_id})
                )
            )
            for trans_obj in resp.json():
                if cls.get_trans_release(trans_obj['_id']) == 'true':
                    return 'true'
        return 'false'

    @classmethod
    def get_user_release(cls, user_id):
        """Get the user release from transactions on that proj."""
        for trans_rel in ['transsip', 'transsap']:
            resp = requests.get(
                text_type('{base_url}/{trans_rel}?{args}').format(
                    trans_rel=trans_rel,
                    base_url=get_config().get('metadata', 'endpoint_url'),
                    args=cls.merge_get_args({'submitter': user_id})
                )
            )
            for trans_obj in resp.json():
                if cls.get_trans_release(trans_obj['_id']) == 'true':
                    return 'true'
        return 'false'

    @classmethod
    def get_institutions_from_user(cls, user_id):
        """Get an institution list based on user id."""
        key = text_type('inst_by_user_{}').format(user_id)
        val = cls.obj_cache.get(key, None)
        if val is not None:
            return val

        resp = requests.get(
            text_type('{base_url}/institution_user?{args}').format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                args=cls.merge_get_args({'user': user_id})
            )
        )
        ret = []
        for inst_id in [obj['institution'] for obj in resp.json()]:
            ret.append(cls.render('institutions',
                                  cls.get_obj_by_id('institutions', inst_id)))
        cls.obj_cache[key] = ret
        return ret

    @classmethod
    def get_groups_from_instrument(cls, inst_id):
        """Get the list of groups from an instrument."""
        key = text_type('grp_by_inst_{}').format(inst_id)
        val = cls.obj_cache.get(key, None)
        if val is not None:
            return val

        url = '{base_url}/instrument_group?' + \
            cls.merge_get_args({'instrument': '{inst_id}'})
        resp = requests.get(
            text_type(url).format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                inst_id=inst_id
            )
        )
        ret = []
        for grp_id in [obj['group'] for obj in resp.json()]:
            ret.append(cls.render(
                'groups', cls.get_obj_by_id('groups', grp_id)))
        cls.obj_cache[key] = ret
        return ret

    @classmethod
    def get_transactions_from_keys(cls, _key_id):
        """Get a list of transactions for a specific key."""
        return []

    @classmethod
    def get_transactions_from_values(cls, _value_id):
        """Get a list of transactions for a specific value."""
        return []

    # pylint: disable=invalid-name
    @classmethod
    def get_transactions_from_institutions(cls, inst_id):
        """Get a list of transactions from an institution."""
        key = text_type('trans_by_instit_{}').format(inst_id)
        val = cls.obj_cache.get(key, None)
        if val is not None:
            return val

        url = '{base_url}/institution_user?' + \
            cls.merge_get_args({'institution': '{inst_id}'})
        resp = requests.get(
            text_type(url).format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                inst_id=inst_id
            )
        )
        ret = []
        for user_id in [obj['user'] for obj in resp.json()]:
            ret.extend(cls.get_transactions_from_users(user_id))
        cls.obj_cache[key] = ret
        return ret
    # pylint: enable=invalid-name

    @classmethod
    def get_transactions_from_users(cls, user_id):
        """Get a list of transactions for a user."""
        key = text_type('trans_by_user_{}').format(user_id)
        val = cls.obj_cache.get(key, None)
        if val is not None:
            return val

        ret = set()
        for trans_rel in ['transsip', 'transsap']:
            url = '{base_url}/{trans_rel}?' + \
                cls.merge_get_args({'submitter': '{user_id}'})
            resp = requests.get(
                text_type(url).format(
                    trans_rel=trans_rel,
                    base_url=get_config().get('metadata', 'endpoint_url'),
                    user_id=user_id
                )
            )
            ret.update(set(['transactions_{}'.format(
                obj['_id']) for obj in resp.json()]))
        cls.obj_cache[key] = list(ret)
        return cls.obj_cache[key]

    @classmethod
    def get_transactions_from_projects(cls, proj_id):
        """Get a list of transactions for a project."""
        key = text_type('trans_by_proj_{}').format(proj_id)
        val = cls.obj_cache.get(key, None)
        if val is not None:
            return val

        ret = set()
        for trans_rel in ['transsip', 'transsap']:
            url = '{base_url}/{trans_rel}?' + \
                cls.merge_get_args({'project': '{proj_id}'})
            resp = requests.get(
                text_type(url).format(
                    trans_rel=trans_rel,
                    base_url=get_config().get('metadata', 'endpoint_url'),
                    proj_id=proj_id
                )
            )
            ret.update(set(['transactions_{}'.format(
                obj['_id']) for obj in resp.json()]))
        cls.obj_cache[key] = list(ret)
        return cls.obj_cache[key]

    # pylint: disable=invalid-name
    @classmethod
    def get_transactions_from_instruments(cls, inst_id):
        """Get a list of transactions for a instrument."""
        key = text_type('trans_by_inst_{}').format(inst_id)
        val = cls.obj_cache.get(key, None)
        if val is not None:
            return val

        url = '{base_url}/transsip?' + \
            cls.merge_get_args({'instrument': '{inst_id}'})
        resp = requests.get(
            text_type(url).format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                inst_id=inst_id
            )
        )
        cls.obj_cache[key] = ['transactions_{}'.format(
            obj['_id']) for obj in resp.json()]
        return cls.obj_cache[key]
    # pylint: enable=invalid-name

    @classmethod
    def get_transactions_from_groups(cls, group_id):
        """Get a list of instruments for a group."""
        key = text_type('trans_by_group_{}').format(group_id)
        val = cls.obj_cache.get(key, None)
        if val is not None:  # pragma: no cover
            return val

        url = '{base_url}/instrument_group?' + \
            cls.merge_get_args({'group': '{group_id}'})
        resp = requests.get(
            text_type(url).format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                group_id=group_id
            )
        )
        ret = []
        for inst_id in [obj['instrument'] for obj in resp.json()]:
            ret.extend(cls.get_transactions_from_instruments(inst_id))
        cls.obj_cache[key] = ret
        return ret

    # pylint: disable=invalid-name
    @classmethod
    def get_transactions_from_science_theme(cls, science_theme):
        """Get a list of transactions for a science theme."""
        key = text_type('trans_by_sci_{}').format(science_theme)
        val = cls.obj_cache.get(key, None)
        if val is not None:
            return val

        url = '{base_url}/projects?' + \
            cls.merge_get_args({'science_theme': '{science_theme}'})
        resp = requests.get(
            text_type(url).format(
                base_url=get_config().get('metadata', 'endpoint_url'),
                science_theme=science_theme
            )
        )
        ret = []
        for proj_id in [obj['_id'] for obj in resp.json()]:
            ret.extend(cls.get_transactions_from_projects(proj_id))
        cls.obj_cache[key] = ret
        return ret
    # pylint: enable=invalid-name

    @classmethod
    def generate(cls, obj_cls, objs, trans_ids=False, render_release=False):
        """generate the institution object."""
        for obj in objs:
            yield {
                '_op_type': 'update',
                '_index': ELASTIC_INDEX,
                '_type': 'doc',
                '_id': text_type('{}_{}').format(obj_cls, obj['_id']),
                'doc': cls.render(obj_cls, obj, trans_ids, render_release),
                'doc_as_upsert': True
            }
            if obj_cls == 'projects':
                yield {
                    '_op_type': 'update',
                    '_index': ELASTIC_INDEX,
                    '_type': 'doc',
                    '_id': text_type('science_theme_{}').format(obj['science_theme']),
                    'doc': cls.render_science_theme(obj, trans_ids),
                    'doc_as_upsert': True
                }

    @classmethod
    def render_science_theme(cls, obj, trans_ids=False):
        """Render the science theme as an object..."""
        ret = {
            'type': 'science_theme',
            'obj_id': text_type('science_theme_{}').format(obj['science_theme']),
            'display_name': obj['science_theme']
        }
        if trans_ids:
            ret['transaction_ids'] = cls.get_transactions_from_science_theme(
                obj['science_theme']
            )
        return ret

    @classmethod
    def render(cls, obj_cls, obj, trans_ids=False, render_release=False):
        """Render the instrument object hash."""
        ret = {
            'type': obj_cls
        }
        for key, value in cls.render_data[obj_cls].items():
            if key == 'release' and not render_release:
                continue
            if callable(value):
                ret[key] = value(obj)
            else:
                if value.format(**obj) == 'None':
                    ret[key] = None
                else:
                    ret[key] = value.format(**obj)
        if trans_ids:
            trans_func = getattr(
                cls, 'get_transactions_from_{}'.format(obj_cls))
            ret['transaction_ids'] = trans_func(obj['_id'])
        return ret
# pylint: enable=too-many-public-methods
