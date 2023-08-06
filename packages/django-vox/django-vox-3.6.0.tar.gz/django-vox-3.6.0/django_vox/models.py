import abc
import collections
import inspect
import json
import random
import uuid
import warnings
from typing import List, Mapping, TypeVar, cast

import aspy
import dateutil.parser
import django.conf
import django.utils.timezone
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import NOT_PROVIDED, Q
from django.template import Context
from django.utils.translation import ugettext_lazy as _

import django_vox.backends
from django_vox.backends.base import AttachmentData

from . import base, registry, settings

__all__ = ('find_activity_type', 'get_model_from_relation',
           'resolve_parameter', 'make_model_preview', 'PreviewParameters',
           'get_model_variables', 'get_model_attachment_choices',
           'AbstractContactable', 'VoxOptions', 'VoxModelBase', 'VoxModel',
           'VoxNotification', 'VoxNotifications', 'VoxAttach',
           'VoxAttachments', 'NotificationManager', 'Notification',
           'Template', 'TemplateAttachment', 'SiteContactManager',
           'OneTimeNotification',
           'SiteContact', 'SiteContactSetting', 'FailedMessage', 'InboxItem')


def load_aspy_object(json_str):
    data = json.loads(json_str)
    return _load_aspy_object(data)


def _load_aspy_object(data):
    obj = getattr(aspy, data.get('type', 'Object'))()
    for key, value in data.items():
        if key not in ('type', '@context'):
            if aspy.PROPERTIES.get(key) is aspy.datetime_property:
                value = dateutil.parser.parse(value)
            if isinstance(value, dict):
                value = _load_aspy_object(value)
            obj[key] = value
    return obj


def find_activity_type(url):
    if ':' not in url:
        url = aspy.as_uri(url)
    for item in aspy.__dict__.values():
        if inspect.isclass(item):
            if issubclass(item, (aspy.Object, aspy.Link)):
                if item.get_type() == url:
                    return item


def make_activity_object(obj):
    iri = None
    # if obj.__class__ in registry.objects:
    address_func = getattr(obj, 'get_object_address')
    if address_func:
        iri = obj.get_object_address()
    if iri is None and hasattr(obj, 'get_absolute_url'):
        iri = django_vox.base.full_iri(obj.get_absolute_url())
    name = str(obj)
    if iri is None:
        return aspy.Object(name=name)
    return aspy.Object(name=name, id=iri)


def get_model_from_relation(field):
    # code copied from django's admin
    if not hasattr(field, 'get_path_info'):
        raise RuntimeError('Field is not a relation')
    return field.get_path_info()[-1].to_opts.model


def resolve_parameter(key, parameters):
    remainder, _, last = key.rpartition('.')
    parts = remainder.split('.')
    for part in parts:
        try:
            contains = part in parameters
        except TypeError:
            contains = False
        if contains:
            parameters = parameters[part]
        elif hasattr(parameters, part):
            parameters = getattr(parameters, part)
        else:
            return None
    if hasattr(parameters.__class__, '_vox_meta'):
        meta = parameters.__class__._vox_meta
        if last in meta.attachments:
            return meta.attachments[last].get_data(parameters)
    return None


def make_model_preview(object_type):
    obj = object_type.objects.first()
    if obj is not None:
        return obj
    obj = object_type()
    for field in object_type._meta.fields:
        value = None
        if field.default != NOT_PROVIDED:
            value = field.default
        else:
            desc = str(field.description).lower()
            if desc.startswith('string'):
                value = '{{{}}}'.format(field.verbose_name)
            elif desc.startswith('integer'):
                value = random.randint(1, 100)
            else:
                pass
        setattr(obj, field.attname, value)
    return obj


class PreviewParameters:

    def __init__(self, object_type, actor_type, target_type):
        self.target = (make_model_preview(target_type)
                       if target_type else {})
        self.actor = (make_model_preview(actor_type)
                      if actor_type else {})
        self.object = make_model_preview(object_type)
        # for backwards compatibility
        self.source = self.actor
        self.content = self.object

    def __contains__(self, item):
        return item in ('contact', 'target', 'actor', 'object',
                        'content', 'source')

    def __getitem__(self, attr):
        return getattr(self, attr)


def get_model_variables(label, value, cls, ancestors=set()):
    assert issubclass(cls, models.Model)
    sub_ancestors = ancestors.copy()
    sub_ancestors.add(cls)
    attrs = []
    skip_relations = len(ancestors) > 2
    children = []
    for field in cls._meta.fields:
        sub_label = field.verbose_name.title()
        sub_value = '{}.{}'.format(value, field.name)
        if field.is_relation:
            model = get_model_from_relation(field)
            # prevent super long/circular references
            if skip_relations or model in ancestors:
                continue
            children.append(get_model_variables(
                sub_label, sub_value, model, ancestors=sub_ancestors))
        else:
            attrs.append({'label': sub_label, 'value': sub_value})
    return {'label': label, 'value': value, 'attrs': attrs,
            'rels': children}


def get_model_attachment_choices(label, value, cls, ancestors=set()):
    sub_ancestors = ancestors.copy()
    sub_ancestors.add(cls)
    if hasattr(cls, '_vox_meta'):
        fields = cls._vox_meta.attachments
        for field in fields:
            label = ('{}/{}'.format(label, field.label)
                     if label else field.label)
            yield (value + '.' + field.key), label
    if hasattr(cls, '_meta') and len(sub_ancestors) < 3:
        for field in cls._meta.fields:
            if field.is_relation:
                model = get_model_from_relation(field)
                if model not in ancestors:
                    sub_label = field.verbose_name.title()
                    sub_label = ('{}/{}'.format(label, sub_label)
                                 if label else sub_label)
                    sub_value = '{}.{}'.format(value, field.name)
                    yield from get_model_attachment_choices(
                        sub_label, sub_value, field.related_model,
                        ancestors=sub_ancestors)


class AbstractContactable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_contacts_for_notification(
            self, notification: 'Notification') -> List[base.Contact]:
        ...


class VoxOptions(object):
    """
    Options for Vox extensions
    """

    ALL_OPTIONS = ('notifications', 'attachments')
    # list of notification code names
    notifications = []
    attachments = {}

    def __init__(self, meta):
        """
        Set any options provided, replacing the default values
        """
        if meta is not None:
            for key, value in meta.__dict__.items():
                if key in self.ALL_OPTIONS:
                    setattr(self, key, value)
                elif not key.startswith('_'):  # ignore private parts
                    raise ValueError(
                        'VoxMeta has invalid attribute: {}'.format(key))


class VoxModelBase(models.base.ModelBase):
    """
    Metaclass for Vox extensions.

    Deals with notifications on VoxOptions
    """
    def __new__(mcs, name, bases, attributes):
        new = super(VoxModelBase, mcs).__new__(
            mcs, name, bases, attributes)
        meta = attributes.pop('VoxMeta', None)
        setattr(new, '_vox_meta', VoxOptions(meta))
        return new


VoxModelN = TypeVar('VoxModelN', 'VoxModel', None)


class VoxModel(models.Model, metaclass=VoxModelBase):
    """
    Base class for models that implement notifications
    """

    class Meta:
        abstract = True

    @classmethod
    def get_notification(cls, codename: str) -> 'Notification':
        ct = ContentType.objects.get_for_model(cls)
        return Notification.objects.get(
            codename=codename, object_type=ct)

    def issue_notification(self, codename: str,
                           target: VoxModelN = None,
                           actor: VoxModelN = None):
        notification = self.get_notification(codename)
        notification.issue(self, target, actor)

    def get_activity_object(self, codename, actor, target):
        """Return an aspy.Object object for the activity.

        The parameters actor and target may be None.
        """
        return self.__activity__()

    def get_object_address(self):
        if self.__class__ not in registry.objects:
            raise RuntimeError(
                '{cls} is not a registered object, use '
                'django_vox.registry.object.add({cls}, regex=...)'.format(
                    cls=self.__class__))
        url = registry.objects[self.__class__].reverse(self)
        if url is None:
            return None
        return django_vox.base.full_iri(url)

    def __activity__(self):
        return make_activity_object(self)


class VoxNotifications(list):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if not isinstance(value, VoxNotification):
                value = VoxNotification(value)
            if not value.params['codename']:
                value.params['codename'] = key
            self.append(value)


class VoxNotification:
    REQUIRED_PARAMS = {'codename', 'description'}
    OPTIONAL_PARAMS = {'actor_type': '', 'target_type': '',
                       'activity_type': 'Create', 'required': False}

    def __init__(self, description, codename='', **kwargs):
        self.params = {
            'codename': codename,
            'description': description,
            'from_code': True,
        }
        for key, default in self.OPTIONAL_PARAMS.items():
            if key in kwargs:
                self.params[key] = kwargs.pop(key)
            else:
                self.params[key] = default
        if kwargs:
            raise ValueError('Unrecognized parameters {}'.format(
                ', '.join(kwargs.keys())))

    def params_equal(self, notification):
        for key in self.params:
            value = getattr(notification, key)
            my_value = self.params[key]
            if key in ('actor_type', 'target_type'):
                if value is None:
                    value = ''
                else:
                    value = '{}.{}'.format(value.app_label, value.model)
            # if key == 'activity_type':
            #     value = value.get_type()
            if value != my_value:
                return False
        return True

    def param_value(self, key):
        value = self.params[key]
        if key in ('actor_type', 'target_type'):
            if value == '':
                return None
            model = apps.get_model(value)
            return ContentType.objects.get_for_model(model)
        if key == 'activity_type':
            if inspect.isclass(value) and issubclass(value, aspy.Object):
                value = value.get_type()
        return value

    def set_params(self, notification):
        for key in self.params:
            setattr(notification, key, self.param_value(key))

    def create(self, object_type):
        new = Notification(object_type=object_type)
        self.set_params(new)
        return new

    @property
    def codename(self):
        return self.params['codename']


# Temporarily here for backwards compatibility
class VoxParam(VoxNotification):

    def __init__(self, codename, description, **kwargs):
        super().__init__(description, codename=codename, **kwargs)


class VoxAttach:
    def __init__(self, attr: str = None,
                 mime_attr: str = '', mime_string: str = '', label=''):
        self.key = ''  # gets set later
        self.attr = attr
        if bool(mime_attr) == bool(mime_string):
            raise RuntimeError(
                'Either mime_attr must be set or mime_string (not both)')
        self.mime_attr = mime_attr
        self.mime_string = mime_string
        self._label = label

    @property
    def label(self):
        return self._label if self._label else self.key

    def get_data(self, model_instance: VoxModel):
        data = getattr(model_instance, self.attr)
        if callable(data):
            data = data()
        # force bytes
        if not isinstance(data, bytes):
            if not isinstance(data, str):
                data = str(data)
            data = data.encode()
        if self.mime_attr:
            mime = getattr(model_instance, self.mime_attr)
            if callable(mime):
                mime = mime()
        else:
            mime = self.mime_string
        return AttachmentData(data, mime)


class VoxAttachments:
    def __init__(self, **kwargs: Mapping[str, VoxAttach]):
        self.items = {}
        for key, value in kwargs.items():
            value.key = key
            if value.attr is None:
                value.attr = key
            self.items[key] = value

    def __iter__(self):
        yield from self.items.values()

    def __contains__(self, item: str):
        return self.items.__contains__(item)

    def __getitem__(self, item: str):
        return self.items.__getitem__(item)


class ChannelContactSet:

    def __init__(self, notification, obj, target, actor):
        # make a dictionary where the keys are protocol, 'recipient key'
        # pairs, the values are address => contactable dictionaries
        channels = notification.get_recipient_channels(obj, target, actor)
        self._set = collections.defaultdict(dict)
        contactable_list = dict((key, channel.contactables())
                                for (key, channel) in channels.items())
        for recipient_key, contactables in contactable_list.items():
            for c_able in contactables:
                for contact in c_able.get_contacts_for_notification(
                        notification):
                    self._set[contact.protocol, recipient_key][
                        contact.address] = c_able

    def get_addresses(self, protocol: str, recipients: List[str]):
        for recipient in recipients:
            if (protocol, recipient) in self._set:
                yield from self._set[protocol, recipient].keys()

    def get_address_items(self, protocol: str, recipients: List[str]):
        for recipient in recipients:
            if (protocol, recipient) in self._set:
                yield from self._set[protocol, recipient].items()


class NotificationManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, app_label, model, codename):
        return self.get(
            codename=codename,
            object_type=ContentType.objects.db_manager(
                self.db).get_by_natural_key(app_label, model),
        )


class Notification(models.Model):
    """
    Base class for all notifications
    """

    codename = models.CharField(_('codename'), max_length=100)
    object_type = models.ForeignKey(
        to=ContentType, on_delete=models.CASCADE,
        limit_choices_to=registry.channel_type_limit,
        verbose_name=_('object type'))
    description = models.TextField(_('description'))
    actor_type = models.ForeignKey(
        to=ContentType, on_delete=models.CASCADE, related_name='+',
        limit_choices_to=registry.channel_type_limit,
        verbose_name=_('actor model'), null=True, blank=True)
    target_type = models.ForeignKey(
        to=ContentType, on_delete=models.CASCADE, related_name='+',
        limit_choices_to=registry.channel_type_limit,
        verbose_name=_('target model'), null=True, blank=True)
    required = models.BooleanField(
        _('required'), default=False,
        help_text=_('If true, triggering the notification will throw an '
                    'error if there is no available template/contact'))
    activity_type = models.URLField(
        _('activity type'), default='', blank=True,
        help_text=_('Full URL for activity type (i.e. '
                    'https://www.w3.org/ns/activitystreams#Object)')
    )
    from_code = models.BooleanField(
        _('from code'), default=False,
        help_text=_('True if the notification is defined in the code and '
                    'automatically managed'))

    objects = NotificationManager()

    def __str__(self):
        return "{} | {} | {}".format(
            self.object_type.app_label, self.object_type, self.codename)

    def natural_key(self):
        return self.object_type.natural_key() + (self.codename,)

    natural_key.dependencies = ['contenttypes.contenttype']

    def get_recipient_models(self):
        recipient_spec = {
            'si': SiteContact,
            're': self.get_target_type(),
            'se': self.get_actor_type(),
            'c': self.get_object_model(),
        }
        return dict((key, value) for (key, value)
                    in recipient_spec.items() if value is not None)

    def get_parameter_models(self):
        spec = {
            'target': self.get_target_type(),
            'actor': self.get_actor_type(),
            'object': self.get_object_model(),
        }
        return dict((key, value) for (key, value)
                    in spec.items() if value is not None)

    def get_recipient_instances(self, obj, target, actor):
        choices = {
            'si': SiteContact(),
            'c': obj,
        }
        if self.target_type and (target is not None):
            choices['re'] = target
        elif self.target_type:
            raise RuntimeError(
                'Model specified "target_type" for notification but '
                'target missing on issue_notification ')
        elif target is not None:
            raise RuntimeError('Target added to issue_notification, '
                               'but is not specified in VoxMeta')
        if self.actor_type and (actor is not None):
            choices['se'] = actor
        elif self.actor_type:
            raise RuntimeError(
                'Model specified "actor_type" for notification but actor '
                'missing on issue_notification ')
        elif actor is not None:
            raise RuntimeError('Actor added to issue_notification, but is '
                               'not specified in VoxMeta')

        return dict((key, model) for (key, model)
                    in choices.items() if model is not None)

    def get_recipient_channels(self, obj, target, actor)\
            -> Mapping[str, registry.Channel]:
        instances = self.get_recipient_instances(obj, target, actor)
        return dict((key, channel)
                    for recip_key, model in instances.items()
                    for key, channel in registry.objects[
                        model.__class__].channels.prefix(
                            recip_key).bind(model).items())

    def get_recipient_choices(self):
        recipient_models = self.get_recipient_models()
        for recipient_key, model in recipient_models.items():
            channel_data = registry.objects[model].channels.prefix(
                recipient_key)
            for key, channel in channel_data.items():
                yield key, channel.name

    def _get_activity_object(self, obj, actor, target):
        if hasattr(obj, 'get_activity_object'):
            return obj.get_activity_object(self.codename, actor, target)
        if hasattr(obj, '__activity__'):
            return obj.__activity__()
        return make_activity_object(obj)

    def issue(self, obj: VoxModel,
              target: VoxModelN = None,
              actor: VoxModelN = None):
        """
        To send a notification to a user, get all the user's active methods.
        Then get the backend for each method and find the relevant template
        to send (and has the said notification). Send that template with
        the parameters with the backend.

        :param obj: model object that the notification is about
        :param target: either a user, or None if no logical target
        :param actor: user who initiated the notification
        :return: None
        """
        # check
        parameters = {
            'content': obj,
            'object': obj,
            'notification': self,
        }
        if target is not None:
            parameters['target'] = target
        if actor is not None:
            parameters['actor'] = actor
            # backwards compatibility
            parameters['source'] = actor

        parameters['activity_object'] = self._get_activity_object(
            obj, actor, target)
        parameters['activity_type'] = self.get_activity_type()
        # load up all the templates so we can see available recipients
        templates = self.template_set.filter(enabled=True)
        contact_set = ChannelContactSet(self, obj, target, actor)

        exceptions = []
        sent = False

        backend_ids = {template.backend for template in templates}
        loaded_backends = dict((bid, django_vox.registry.backends.by_id(bid)())
                               for bid in backend_ids)

        for template in templates:
            backend = loaded_backends[template.backend]
            recipients = template.recipients.split(',')
            # items is a list of address list, contactable pairs
            if template.bulk:
                items = ((contact_set.get_addresses(
                    backend.PROTOCOL, recipients), None),)
            else:
                items = list(((address,), contactable) for
                             (address, contactable) in
                             contact_set.get_address_items(
                                 backend.PROTOCOL, recipients))
            for addresses, contactable in items:
                if contactable is not None:
                    local_params = parameters.copy()
                    local_params['recipient'] = contactable
                else:
                    local_params = parameters

                exception = self.send_message(
                    addresses, local_params, template, backend)
                if exception is None:
                    sent = True
                elif settings.THROW_EXCEPTIONS:
                    exceptions.append(exception)
                else:
                    warnings.warn(RuntimeWarning(exception))

        if exceptions:
            raise exceptions[0]

        if not sent and self.required:
            raise RuntimeError('Notification required, but no message sent')

    @staticmethod
    def send_message(addresses: List[str],
                     parameters: dict, template, backend) -> Exception:
        attachments = []
        if backend.USE_ATTACHMENTS:
            for attachment in template.attachments.all():
                data = resolve_parameter(attachment.key, parameters)
                if data is not None:
                    attachments.append(data)
        message = backend.build_message(
            template.subject, template.content, parameters, attachments)
        from_address = backend.get_from_address(
            template.from_address, parameters)
        # We're catching all exceptions here because some people
        # are bad people and can't subclass properly
        try:
            backend.send_message(from_address, addresses, message)
        except Exception as e:
            FailedMessage.objects.create(
                backend=backend.ID,
                from_address=from_address,
                to_addresses=','.join(addresses),
                message=str(message),
                error=str(e),
            )
            return e
        return None

    def can_issue_custom(self):
        return not (self.actor_type or self.target_type)

    def preview(self, backend_id, message):
        backend = registry.backends.by_id(backend_id)
        params = PreviewParameters(
            self.get_object_model(), self.get_actor_type(),
            self.get_target_type())
        return backend.preview_message('', message, params)

    def get_actor_type(self):
        return (self.actor_type.model_class() if self.actor_type_id
                else None)

    def get_target_type(self):
        return (self.target_type.model_class() if self.target_type_id
                else None)

    def get_object_model(self):
        return (self.object_type.model_class() if self.object_type_id
                else None)

    def get_activity_type(self):
        if self.activity_type == '':
            return aspy.Create
        return find_activity_type(self.activity_type)

    def get_recipient_variables(self):
        recipient_spec = self.get_recipient_models()
        actor_type = self.get_actor_type()
        target_type = self.get_target_type()
        content_model = self.get_object_model()
        mapping = {}
        for target_key, model in recipient_spec.items():
            if model is not None:
                channels = registry.objects[model].channels.prefix(target_key)
                for key, channel in channels.items():
                    label = str(_('Recipient {}')).format(channel.name)
                    mapping[key] = get_model_variables(
                        label, 'recipient', channel.target_class)
        content_name = content_model._meta.verbose_name.title()
        mapping['_static'] = [
            get_model_variables(content_name, 'object', content_model),
        ]
        if actor_type:
            mapping['_static'].append(
                get_model_variables('Actor', 'actor', actor_type))
        if target_type:
            mapping['_static'].append(
                get_model_variables('Target', 'target', target_type))
        return mapping


class _OneTimeNotificationType:
    codename = ''
    object_type_id = None
    description = ''
    actor_type_id = None
    target_type_id = None
    required = True
    activity_type = 'Object'
    from_code = False

    def __str__(self):
        return '<OneTimeNotification>'

    @property
    def object_type(self):
        return None

    @property
    def actor_type(self):
        return None

    @property
    def target_type(self):
        return None

    def natural_key(self):
        return '', '', ''

    def get_actor_type(self):
        return None

    def get_target_type(self):
        return None

    def get_object_model(self):
        return None

    def get_activity_type(self):
        return aspy.Create

    def get_recipient_variables(self):
        return {}

    def send(self, backend_id, contacts, from_address, subject, body):
        backend = django_vox.registry.backends.by_id(backend_id)()
        to_addresses = [c.address for c in contacts
                        if c.protocol == backend.PROTOCOL]

        parameters = {}
        message = backend.build_message(
            subject, body, parameters, attachments=[])
        from_address = backend.get_from_address(from_address, parameters)
        try:
            backend.send_message(from_address, to_addresses, message)
        except Exception as e:
            FailedMessage.objects.create(
                backend=backend.ID,
                from_address=from_address,
                to_addresses=','.join(to_addresses),
                message=str(message),
                error=str(e),
            )
            return e
        return None


OneTimeNotification = _OneTimeNotificationType()


class Template(models.Model):

    class Meta:
        verbose_name = _('template')

    notification = models.ForeignKey(
        to=Notification, on_delete=models.PROTECT,
        verbose_name=_('notification'))
    backend = models.CharField(_('backend'), max_length=100)
    subject = models.CharField(_('subject'), max_length=500, blank=True)
    content = models.TextField(_('content'))
    recipients = models.TextField(
        verbose_name=_('recipients'), default='re', blank=True,
        help_text=_('Who this message actually gets sent to.'))
    from_address = models.CharField(
        _('from address'), max_length=500, blank=True)
    enabled = models.BooleanField(
        _('enabled'), default=True,
        help_text=_('When not active, the template will be ignored'))
    bulk = models.BooleanField(
        _('bulk'), default=True,
        help_text=_('Send the same message to all recipients'))

    objects = models.Manager()

    def render(self, parameters: dict, autoescape=True):
        content = cast(str, self.content)
        template = django_vox.backends.base.template_from_string(content)
        context = Context(parameters, autoescape=autoescape)
        return template.render(context)

    def __str__(self):
        choices = {}
        if self.notification:
            choices = dict(self.notification.get_recipient_choices())
        recipients = ', '.join(str(choices.get(r, r)) for r
                               in self.recipients.split(','))
        backend = registry.backends.by_id(self.backend)
        return '{} for {}'.format(backend.VERBOSE_NAME, recipients)


class TemplateAttachment(models.Model):

    class Meta:
        verbose_name = _('template attachment')

    template = models.ForeignKey(
        to=Template, on_delete=models.CASCADE,
        verbose_name=_('template'), related_name='attachments')
    key = models.CharField(_('key'), max_length=500)


class SiteContactManager(models.Manager, AbstractContactable):
    use_in_migrations = True

    def get_contacts_for_notification(
            self, notification: 'Notification') -> List[base.Contact]:
        wlq = Q(enable_filter='whitelist',
                sitecontactsetting__notification=notification,
                sitecontactsetting__enabled=True)
        blq = Q(enable_filter='blacklist') & ~Q(
                sitecontactsetting__notification=notification,
                sitecontactsetting__enabled=False)
        for sc in SiteContact.objects.filter(blq | wlq).distinct():
            yield base.Contact(sc.name, sc.protocol, sc.address)


# can't make this subclass AbstractContact or fields become unset-able
class SiteContact(VoxModel):

    ENABLE_CHOICES = (
        ('blacklist', _('Blacklist')),
        ('whitelist', _('Whitelist')),
    )

    class Meta:
        verbose_name = _('site contact')
        unique_together = (('address', 'protocol'),)

    name = models.CharField(_('name'), blank=True, max_length=500)
    protocol = models.CharField(_('protocol'), max_length=100)
    address = models.CharField(_('address'), max_length=500, blank=True)
    enable_filter = models.CharField(choices=ENABLE_CHOICES, max_length=10,
                                     default='blacklist')

    objects = SiteContactManager()

    def __str__(self):
        return self.name

    @staticmethod
    def all_contacts(_obj):
        yield SiteContact.objects


class SiteContactSetting(models.Model):

    class Meta:
        verbose_name = _('site contact setting')
        unique_together = (('site_contact', 'notification'),)

    site_contact = models.ForeignKey(SiteContact, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    enabled = models.BooleanField(_('enabled'))

    objects = models.Manager()


class FailedMessage(models.Model):

    class Meta:
        verbose_name = _('failed message')

    backend = models.CharField(_('backend'), max_length=100)
    from_address = models.CharField(_('from address'),
                                    max_length=500, blank=True)
    to_addresses = models.TextField(_('to addresses'))
    message = models.TextField(_('message'))
    error = models.TextField(_('error'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return '{} @ {}'.format(self.to_addresses, self.created_at)

    def resend(self):
        backend = django_vox.registry.backends.by_id(self.backend)()
        to_addresses = list(self.to_addresses.split(','))
        backend.send_message(self.from_address, to_addresses, self.message)
        self.delete()


class Activity(models.Model):
    id = models.UUIDField(
        _('ID'), primary_key=True, serialize=True, default=uuid.uuid4)
    name = models.CharField(
        _('name'), max_length=512, blank=True)
    summary = models.TextField(blank=True)
    type = models.CharField(
        _('type'), max_length=512, db_index=True)
    # the json fields should be able to be referenced and
    # repopulated by the id fields
    actor_id = models.CharField(
        _('actor id'), max_length=2048, db_index=True)
    actor_json = models.TextField(blank=True)
    target_id = models.CharField(
        _('target id'), max_length=2048, db_index=True)
    target_json = models.TextField(blank=True)
    object_id = models.CharField(
        _('object id'), max_length=2048, db_index=True)
    object_json = models.TextField(blank=True)
    # and a timestamp, maybe useful
    timestamp = models.DateTimeField(
        _('timestamp'), db_index=True, auto_now_add=True)

    def get_full_url(self):
        return django_vox.base.full_iri(
            registry.objects[Activity].reverse(self))

    def __activity__(self):
        # this is a bit hackish because we're using dicts and not aspy
        # objects
        aspy_class = getattr(aspy, self.type, aspy.Object)
        obj = aspy_class(id=self.get_full_url(), published=self.timestamp)
        for field in ('actor', 'object', 'target'):
            value = getattr(self, field + '_json')
            if value:
                obj[field] = load_aspy_object(value)
        for field in 'summary', 'name':
            value = getattr(self, field)
            if value:
                obj[field] = value
        return obj

    def activity_read(self, _activity, user):
        inbox_item = InboxItem.objects.get(owner=user, activity=self)
        inbox_item.read_at = django.utils.timezone.now()
        inbox_item.save()


class InboxItem(models.Model):

    class Meta:
        unique_together = ('owner', 'activity')

    owner = models.ForeignKey(
        to=django.conf.settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='+',
        verbose_name=_('owner'))
    activity = models.ForeignKey(
        to=Activity, on_delete=models.CASCADE, related_name='+',
        verbose_name=_('activity'))
    read_at = models.DateTimeField(
        _('date read'), db_index=True, null=True, blank=True)


registry.objects.add(SiteContact, regex=None)
registry.objects[SiteContact].channels.add(
    '', '', SiteContact, SiteContact.all_contacts)
registry.objects.add(Activity, regex=settings.ACTIVITY_REGEX)
