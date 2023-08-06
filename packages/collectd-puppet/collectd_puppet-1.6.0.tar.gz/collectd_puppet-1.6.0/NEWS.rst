News
====
2019-04-25 - Release 1.6.0
--------------------------
- Add Puppet5 compat when the catalog does not compile.

2019-02-05 - Release 1.5.1
--------------------------
- Python 3 fix

2019-02-05 - Release 1.5.0
--------------------------
- Pypi auto publish fixed.

2019-01-23 - Release 1.4.3
--------------------------
- Empty release, new pypi pass.

2019-01-23 - Release 1.4.2
--------------------------
- Empty release, first on pypi.

2019-01-23 - Release 1.4.1
--------------------------
- Empty release, first on pypi.

2018-11-07 - Release 1.4.0
--------------------------
- Force a 6 hour retention period of results in collectd.

2018-07-27 - Release 1.3.0
--------------------------
- A schema_version is now published as collectd metadata, set to 1 now.


2018-07-07 - Release 1.2.0
--------------------------
- Add a gauge to puppet_time flagging if the catalog compiled.

2018-07-03 - Release 1.1.1
--------------------------
- Switch to using setup tools.
- Don't send since_last_run, redundant.
- Don't send any data if puppet has not run.

2017-07-21 - Release 1.0.0
--------------------------

-  ``puppet_resources`` metric renamed to ``puppet_run`` metric.
-  ``config_retrieval`` and ``time`` metrics moved from ``puppet_time``
   to ``puppet_run`` type. ``puppet_run`` type only populated if agent
   trys to implement a catalog.

2017-07-14 - Release 0.2.0
--------------------------

-  If compile failiure there is no resources metric.

2017-07-14 - Release 0.1.0
--------------------------

-  First Release
