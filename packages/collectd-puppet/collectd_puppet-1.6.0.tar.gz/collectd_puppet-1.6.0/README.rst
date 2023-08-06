Collectd Plugin for Puppet
==========================

Configuration
-------------

.. code:: apache

   TypesDB "/usr/share/collectd/puppet_types.db"
   <LoadPlugin python>
     Globals true
   </LoadPlugin>

   <Plugin "python">
     LogTraces true
     Interactive false
     Import "puppet"
     PATH "/opt/puppetlabs/puppet/cache/state/last_run_summary.yaml"
   </Plugin>

Collectd Types
--------------

The plugin parses
``/opt/puppetlabs/puppet/cache/state/last_run_summary.yaml`` and reports
two collectd types.

It will only send data if there has been a Puppet run after the last
time Collectd polled. This is monitored using a state file located in
``/var/lib/collectd/puppet.state``. To force a data point just delete
it.

puppet_run
~~~~~~~~~~

A count of numbers of resources and duration of agent run and
config_retrieval

-  total
-  changed
-  corrective_change
-  failed
-  failed_to_restart
-  out_of_sync
-  restarted
-  scheduled
-  skipped
-  time
-  config_retrieval

puppet_time
^^^^^^^^^^^

All in units of seconds

-  last_run - epoch of last puppet run (seconds).
-  compiled - flag denoting if the catalog compiled (1 or 0).

Authors
-------
Steve Traylen <steve.traylen@cern.ch>
Nacho Barrientos <nacho.barrientos@cern.ch>

Copyright
---------
2018 CERN

License
-------
Apache-II License

Development notes
-----------------

Don't forget to bump the ``schema_version`` if you modify the types.
