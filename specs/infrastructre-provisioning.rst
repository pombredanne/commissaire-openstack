..
   This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================
Node Registration
=================



Problem description
===================



::



Design Principles
-----------------
1. Minimum duplication between Commisare-openstack and Commiasre-httpd


Alternatives
------------
1. Use Mistral and Heat


Data model impact
-----------------
None


REST API impact
---------------
1. Add an new API endpoint /infrastructure to the REST API interface.


Security impact
---------------
None


Notifications impact
--------------------
None


Other end user impact
---------------------
None


Performance Impact
------------------


Other deployer impact
---------------------


Developer impact
----------------


Implementation
==============


Assignee(s)
-----------

Primary assignee:
Pete Birley

Other contributors:


Work Items
----------
1. Implement an keystone authoriaztion frontend for Commisaire.


Dependencies
============
Add a dependency to Nova


Testing
=======
Each patch will have unit tests, and Tempest functional tests covered.


Documentation Impact
====================
A set of documentation for this new feature will be required.
