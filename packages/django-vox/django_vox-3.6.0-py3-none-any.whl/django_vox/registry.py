import collections
import pydoc

import django.urls.base
import django.urls.resolvers
import django.utils.encoding
import django.utils.regex_helper
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from django_vox import settings

PROTOCOLS = {
    'email': _('Email'),
    'sms': _('SMS'),
    'slack-webhook': _('Slack Webhook'),
    'json-webhook': _('JSON Webhook'),
    'twitter': _('Twitter'),
    'xmpp': _('XMPP'),
    'activity': _('Activity Stream'),
}

PREFIX_NAMES = {
    'si': _('Site Contacts'),
    'c': '__content__',
    'se': _('Actor'),
    're': _('Target'),
}
PREFIX_FORMATS = {
    'c': '{}',
    'se': _('Actor\'s {}'),
    're': _('Target\'s {}'),
}

_CHANNEL_TYPE_IDS = None


class ObjectNotFound(Exception):
    pass


class BackendManager:

    def __init__(self, class_list):
        self.proto_map = collections.defaultdict(list)
        self.id_map = {}
        for cls in class_list:
            if cls.ID in self.id_map:
                raise RuntimeError(
                    'Conflicting backend IDs: {}'.format(cls.ID))
            self.proto_map[cls.PROTOCOL].append(cls)
            self.id_map[cls.ID] = cls

    def by_protocol(self, protocol: str):
        return self.proto_map[protocol]

    def by_id(self, id_val):
        return self.id_map[id_val]

    def all(self):
        return self.id_map.values()

    def protocols(self):
        return self.proto_map.keys()


UnboundChannel = collections.namedtuple(
    'UnboundChannel', ('name', 'target_class', 'func'))


class Channel:
    def __init__(self, ubc: UnboundChannel, obj):
        self.name = ubc.name
        self.target_class = ubc.target_class
        self.func = ubc.func
        self.obj = obj

    def contactables(self):
        return (self.obj,) if self.func is None else self.func(self.obj)


class UnboundChannelMap(dict):

    def bind(self, obj):
        return BoundChannelMap(
            ((key, Channel(ubc, obj)) for (key, ubc) in self.items()))


class BoundChannelMap(dict):
    pass


class ChannelManagerItem:

    def __init__(self, cls):
        self.cls = cls
        self.__prefixes = {}
        self._channels = collections.defaultdict(dict)

    def __bool__(self):
        return bool(self._channels)

    def add(self, key, name, target_type, func):
        self._channels[key] = name, target_type, func
        self.__prefixes = {}

    def add_self(self):
        self.add('', '', self.cls, None)

    def prefix(self, prefix) -> UnboundChannelMap:
        # get channels by prefix
        if prefix not in self.__prefixes:
            ubc_map = UnboundChannelMap()
            for key, (name, cls, func) in self._channels.items():
                channel_key = prefix if key == '' else prefix + ':' + key
                if name == '':
                    name = PREFIX_NAMES[prefix]
                    if name == '__content__':
                        name = self.cls._meta.verbose_name.title()
                else:
                    name = PREFIX_FORMATS[prefix].format(name)
                ubc_map[channel_key] = UnboundChannel(name, cls, func)
            self.__prefixes[prefix] = ubc_map
        return self.__prefixes[prefix]


class ChannelProxyManager(dict):

    def __missing__(self, key):
        if key not in objects:
            objects.add(key, regex=None)
        return objects[key].channels


class ObjectManagerItem:

    def __init__(self, cls):
        self.cls = cls
        self.pattern = None
        self.matcher = None
        self.reverse_form = None
        self.reverse_params = ()
        self.channels = ChannelManagerItem(cls)

    @property
    def has_url(self):
        return self.matcher is not None

    def set_regex(self, pattern: str):
        self.pattern = pattern
        if hasattr(django.urls.resolvers, 'RegexPattern'):
            self.matcher = django.urls.resolvers.RegexPattern(pattern)
        else:
            self.matcher = django.urls.resolvers.RegexURLPattern(pattern, None)
        normal = django.utils.regex_helper.normalize(pattern)
        self.reverse_form, self.reverse_params = next(iter(normal), ('', ()))

    def match(self, path: str):
        if self.matcher is None:
            return False
        if hasattr(django.urls.resolvers, 'RegexPattern'):
            return self.matcher.match(path)
        return self.matcher.resolve(path)

    def reverse(self, obj):
        if self.reverse_form is None:
            return None
        kwargs = dict(((param, getattr(obj, param, None))
                      for param in self.reverse_params))
        return '/' + (self.reverse_form % kwargs)


class ObjectManager(dict):

    def __missing__(self, key):
        item = ObjectManagerItem(key)
        self[key] = item
        return item

    def __setitem__(self, key, value: ObjectManagerItem):
        super().__setitem__(key, value)

    def __getitem__(self, key) -> ObjectManagerItem:
        return super().__getitem__(key)

    def add(self, cls, *, regex=...):
        if regex is ...:
            raise RuntimeError(
                'Must set regex keyword argument, '
                'use None if object has no URL')
        item = ObjectManagerItem(cls)
        if regex is not None:
            item.set_regex(regex)
        self[cls] = item

    def create_local_object(self, path):
        for key, value in self.items():
            match = value.match(path)
            if match:
                # RegexURLPattern vs RegexPattern
                kwargs = match.kwargs if hasattr(match, 'kwargs') else match[2]
                return key.__class__(**kwargs)
        msg = _('Unable to find class for {}.').format(path)
        raise ObjectNotFound(msg)

    def get_local_object(self, path):
        matched_patterns = []
        for key, value in self.items():
            match = value.match(path)
            if match:
                matched_patterns.append(value.pattern)
                # RegexURLPattern vs RegexPattern
                kwargs = match.kwargs if hasattr(match, 'kwargs') else match[2]
                try:
                    return key.objects.get(**kwargs)
                except key.DoesNotExist:
                    pass
        msg = _('Unable to find object for {}.').format(path)
        if matched_patterns:
            msg = msg + ' ' + _(
                'We tried the following patterns: {}.').format(
                ', '.join(matched_patterns))
        raise ObjectNotFound(msg)


backends = BackendManager(
    pydoc.locate(name) for name in settings.BACKENDS)

channels = ChannelProxyManager()

objects = ObjectManager()


def get_protocol_choices():
    for protocol in backends.protocols():
        yield (protocol, PROTOCOLS.get(protocol, protocol))


def _channel_type_ids():
    for all_models in apps.all_models.values():
        for model in all_models.values():
            if model in objects:
                if objects[model].channels:
                    ct = ContentType.objects.get_for_model(model)
                    yield ct.id


def channel_type_limit():
    global _CHANNEL_TYPE_IDS
    if _CHANNEL_TYPE_IDS is None:
        _CHANNEL_TYPE_IDS = tuple(_channel_type_ids())
    return {'id__in': _CHANNEL_TYPE_IDS}
