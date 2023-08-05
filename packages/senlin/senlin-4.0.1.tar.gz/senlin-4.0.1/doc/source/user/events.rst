..
  Licensed under the Apache License, Version 2.0 (the "License"); you may
  not use this file except in compliance with the License. You may obtain
  a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
  License for the specific language governing permissions and limitations
  under the License.


.. _ref-events:

======
Events
======

An :term:`Event` is a record generated during engine execution. Such an event
captures what has happened inside the senlin-engine. The senlin-engine service
generates event records when it is performing some actions or checking
policies.

An event has a ``level`` property which can be interpreted as the severity
level value of the event:

* 10: interpreted as ``DEBUG`` level. Events at this level can be ignored
  safely by users. For developers they may provide some useful information for
  debugging the code.
* 20: interpreted as ``INFO`` level. Events at this level are mostly about
  notifying that some operations have been successfully performed.
* 30: interpreted as ``WARNING`` level. Events at this level are used to
  signal some unhealthy status or anomalies detected by the engine. These
  events should be monitored and checked when operating a cluster.
* 40: interpreted as ``ERROR`` level. Events at this level signifies some
  failures in engine operations. These event should be monitored and checked
  when operating a cluster. Usually some user intervention is expected to
  recover a cluster from this status.
* 50: interpreted as ``CRITICAL`` level. Events at this level are about
  serious problems encountered by the engine. The engine service may have
  run into some bugs. User intervention is required to do a recovery.

Senlin provides an open architecture for event dispatching. Two of the
built-in dispatchers are ``database`` and ``message``. The ``database``
dispatcher dumps the events into database tables and it is enabled by default.
The ``message`` dispatcher converts the event objects into versioned event
notifications and published on the global message queue. This dispatcher is
by default disabled. To enable it, you can add the following line to the
``[DEFAULT]`` section of the ``senlin.conf`` file and then restart the service 
engine::

 event_dispatchers = message

Based on your deployment settings, you may need to add the following lines to
the ``senlin.conf`` file as well. This lines set ``messaging`` as the default
driver used by the ``oslo.messaging`` package::

  [oslo_messaging_notifications]
  driver = messaging

Note that unprocessed event notifications which are not associated with a
TTL (time to live) value by default will remain queued at the message bus,
please make sure the Senlin event notifications will be subscribed and
processed by some services before enabling the ``message`` dispatcher.

Since the event dispatchers are designed as plug-ins, you can develop your own
event dispatchers and have senlin engine load them on startup. For more
details on developing and plugging in your own event dispatchers, please refer
to the :doc:`../contributor/plugin_guide` document.

The following sections are about examining events when using the ``database``
dispatcher which creates database records when events happen.


Listing Events
~~~~~~~~~~~~~~

The following command lists the events by the Senlin engine::

  $ openstack cluster event list
  +----------+---------------------+---------------+----------+----------------------------+-----------------------+-----------+-------+
  | id       | generated_at        | obj_type      | obj_id   | obj_name                   | action                | status    | level |
  +----------+---------------------+---------------+----------+----------------------------+-----------------------+-----------+-------+
  | 1f72eb5e | 2015-12-17T15:41:48 | NODE          | 427e64f3 | node-7171861e-002          | update                | ACTIVE    | 20    |
  | 20b8eb9a | 2015-12-17T15:41:49 | NODE          | 6da22a49 | node-7171861e-001          | update                | ACTIVE    | 20    |
  | 23721815 | 2015-12-17T15:42:51 | NODEACTION    | 5e9a9d3d | node_delete_3e91023e       | NODE_DELETE           | START     | 20    |
  | 54f9eae4 | 2015-12-17T15:41:36 | CLUSTERACTION | 1bffa11d | cluster_create_7171861e    | CLUSTER_CREATE        | SUCCEEDED | 20    |
  | 7e30df62 | 2015-12-17T15:42:51 | CLUSTERACTION | d3cef701 | cluster_delete_64048b01    | CLUSTER_DELETE        | START     | 20    |
  | bf51f23c | 2015-12-17T15:41:54 | CLUSTERACTION | d4dbbcea | cluster_scale_out_7171861e | CLUSTER_SCALE_OUT     | START     | 20    |
  | c58063e9 | 2015-12-17T15:42:51 | NODEACTION    | b2292bb1 | node_delete_59da99f0       | NODE_DELETE           | START     | 20    |
  | ca7d30c6 | 2015-12-17T15:41:38 | CLUSTERACTION | 0be70b0f | attach_policy_7171861e     | CLUSTER_ATTACH_POLICY | START     | 20    |
  | cfe5d0d7 | 2015-12-17T15:42:51 | CLUSTERACTION | 42cf5baa | cluster_delete_352e1b6b    | CLUSTER_DELETE        | START     | 20    |
  | fe2fc810 | 2015-12-17T15:41:49 | CLUSTERACTION | 0be70b0f | attach_policy_7171861e     | CLUSTER_ATTACH_POLICY | SUCCEEDED | 20    |
  +----------+---------------------+---------------+----------+----------------------------+-----------------------+-----------+-------+

The :program:`openstack cluster event list` command line supports various
options when listing the events.


Sorting the List
----------------

You can specify the sorting keys and sorting direction when list events,
using the option :option:`--sort`. The :option:`--sort` option accepts a
string of format ``key1[:dir1],key2[:dir2],key3[:dir3]``, where the keys used
are event properties and the dirs can be one of ``asc`` and ``desc``. When
omitted, Senlin sorts a given key using ``asc`` as the default direction.

For example, the following command sorts the events using the ``timestamp``
property in descending order::

  $ openstack cluster event list --sort timestamp:desc

When sorting the list of events, you can use one of ``timestamp``, ``level``,
``otype``, ``oname``, ``user``, ``action`` and ``status``.


Filtering the List
------------------

You can filter the list of events using the :option:`--filters``. For example,
the following command filters the event list by the ``otype`` property::

  $ openstack cluster event list --filters otype=NODE

The option :option:`--filters` accepts a list of key-value pairs separated by
semicolon (``;``), where each pair is expected to be of format ``key=val``.
The valid keys for filtering include ``oname``, ``otype``, ``oid``,
``cluster_id``, ``action``, ``level`` or any combination of them.


Paginating the Query results
----------------------------

In case you have a huge collection of events (which is highly likely the case),
you can limit the number of events returned using the option
:option:`--limit <LIMIT>`. For example::

  $ openstack cluster event list --limit 10

Another option you can specify is the ID of an event after which you want to
see the returned list starts. In other words, you don't want to see those
events with IDs that is or come before the one you specify. You can use the
option :option:`--marker <ID>` for this purpose. For example::

  $ openstack cluster event list --limit 20 \
      --marker 2959122e-11c7-4e82-b12f-f49dc5dac270

At most 20 action records will be returned in this example and its UUID comes
after the one specified from the command line.


Showing Details of an Event
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the :program:`senlin` command line to show the details about an
event you are interested in. When specifying the identity of the event, you
can use its name, its ID or its "short ID" . Senlin API and engine will verify
if the identifier you specified can uniquely identify an event. An error
message will be returned if there is no event matching the identifier or if
more than one event matching it.

An example is shown below::

  $ openstack cluster event show 19ba155a
  +---------------+--------------------------------------+
  | Field         | Value                                |
  +---------------+--------------------------------------+
  | action        | delete                               |
  | cluster_id    | ce85d842-aa2a-4d83-965c-2cab5133aedc |
  | generated_at  | 2015-12-17T15:43:26+00:00            |
  | id            | 19ba155a-d327-490f-aa0f-589f67194b2c |
  | level         | 20                                   |
  | location      | None                                 |
  | name          | None                                 |
  | obj_id        | cd9f519a-5589-4cbf-8a74-03b12fd9436c |
  | obj_name      | node-ce85d842-003                    |
  | obj_type      | NODE                                 |
  | project_id    | 42d9e9663331431f97b75e25136307ff     |
  | status        | DELETING                             |
  | status_reason | Deletion in progress                 |
  | timestamp     | 2015-12-17T15:43:26                  |
  | user_id       | 5e5bf8027826429c96af157f68dc9072     |
  +---------------+--------------------------------------+


See Also
~~~~~~~~

* :doc:`Operating Actions <actions>`
