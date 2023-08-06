============
 Activities
============

The activities backend provides support for the `Activity Streams`_ (and very
slightly `ActivityPub`_) standards. Message are stored locally in the database
and are retrievable from an inbox. References to notions like actors and
inboxes refer to the ideas in that standard.

.. _Activity Streams: https://www.w3.org/TR/activitystreams-core/
.. _ActivityPub: https://www.w3.org/TR/2018/REC-activitypub-20180123/


Setting up the activities is fairly involved, and also entirely optional
unless you actually want to use the activity backend. As a result, it’s
got its own documentation. Note that this backend is somewhat experimental.
Don’t use it in production unless you’ve tested it really well and know
what you’re doing.


Settings
========

Because we need to generate full uri/iris (including the domain) and
we need to be able to do it without an HTTP request, we need to
have a way of finding out your domain & scheme. If you're already
using ``django.contrib.sites`` and you have it set up with a
``SITE_ID`` in your settings, that’ll work. Otherwise a simpler
solution is to just set these two settings:

===============  ======================================
``SITE_DOMAIN``  Your site’s domain name
``SITE_SSL``     True if you use HTTPS, False otherwise
===============  ======================================

.. caution:: ``SITE_SSL`` should nearly always be True (the default) unless
   you’re in development testing on localhost.

Also, because this backend isn’t enabled by default, you’ll need to
alter ``DJANGO_VOX_BACKENDS`` and add
``'django_vox.backends.activity.Backend',``. You can see an example on the
:doc:`backends` page.

Registering actors
==================

Like we had to register channels before, now we have to register actors too.
It’s mostly accurate to say that actors should be any users that you want to
be able send/receive activities.

Actors all have endpoints, and inboxes (and some unimplemented things). When
you add an actor you specify the route for his/her endpoint using a regex,
much like you would make a normal Django 1 url route. The parameters in the
regex should correspond to the identifying field in the user. Here’s an
example:

.. code-block:: python

   actors[User].set_regex(r'^users/(?P<username>[0-9]+)/$')

Additionally, you’ll also need to return the activity contact from the
``get_contacts_for_notification`` method for the actors. If you want to
send them all the possible notification, then add the following code:

.. code-block:: python

   def get_contacts_for_notification(self, _notification):
       yield Contact(self.name, 'activity', self.get_object_address())


Setting up models
=================

Just like we had to add a bunch of properties to the models for the basic
features in django_vox, there’s a few more to add to get good results for
the activity stream. These aren’t strictly necessary, but your results will
be pretty plain without them. Code samples of all of these are available in
the test site the comes with django_vox.

First, the notification parameters take a new parameter ``activity_type``.
It can be set to an ``aspy.Activity`` subclass. If it’s not set, django_vox
with either match the notification name to an activity type, or use the
default ‘Create’ type.

.. note:: This code makes use of the ``aspy`` library. It’s a dependency, so
          you should get it automatically, just ``import aspy``.

Second, the object of your activity entries defaults to the plain activity
streams “Object” with an id (based on ``get_absolute_url()`` and a name
(based on ``__str__()``). This is pretty bare-bones to say the least. You can
specify something more colorful by implementing the ``__activity__()`` method
and returning another subclass of ``aspy.Object`` with perhaps a few
properties.

Finally, there’s a few rare cases where the same model might need to give
you different objects for different kinds of notifications. If you need to
do this, you can override ``VoxModel.get_activity_object()``.

.. note:: If your model is registered with ``django_vox.registry.objects``,
          it’s recommended to use ``VoxModel.get_object_address()``
          to get the object’s ID, otherwise you can use
          ``django_vox.base.full_iri(self.get_absolute_url())``.


Accessing the Inboxes
=====================

At this point, you should be able to make up activity notifications, issue
them, and then retrieve them using ``django_vox.models.InboxItem``. However,
if you want to use our hackish ActivityPub half-implementation, there’s one/two
more steps. First we have to enable the inbox middleware. Add this to your
settings.py:

.. code-block:: python

   MIDDLEWARE = [
       ...
       'django_vox.middleware.activity_inbox_middleware',
   ]

There‘s still a few things that remain to be documented, like reading inbox
items, and adding the ability to perform actions on data in your models by
posting to the inbox.
