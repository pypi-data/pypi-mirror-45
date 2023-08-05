OpenStack Dashboard Configuration Guide
=======================================

After installing the Sahara dashboard, there are a few extra configurations
that can be made.

Dashboard configurations are applied through Horizon's local_settings.py file.
The sample configuration file is available `from the Horizon repository. <https://git.openstack.org/cgit/openstack/horizon/tree/openstack_dashboard/local/local_settings.py.example>`_

1. Networking
-------------

Depending on the Networking backend (Nova Network or Neutron) used in the
cloud, Sahara panels will determine automatically which input fields should be
displayed.

While using Nova Network backend the cloud may be configured to automatically
assign floating IPs to instances. If Sahara service is configured to use those
automatically assigned floating IPs the same configuration should be done to
the dashboard through the ``SAHARA_AUTO_IP_ALLOCATION_ENABLED`` parameter.

Example:

.. sourcecode:: python

    SAHARA_AUTO_IP_ALLOCATION_ENABLED = True
..


2. Different endpoint
---------------------

Sahara UI panels normally use ``data-processing`` endpoint from Keystone to
talk to Sahara service. In some cases it may be useful to switch to another
endpoint, for example use locally installed Sahara instead of the one on the
OpenStack controller.

To switch the UI to another endpoint the endpoint should be registered in the
first place.

Local endpoint example:

.. sourcecode:: console

    openstack service create --name sahara_local --description \
        "Sahara Data Processing (local installation)" \
        data_processing_local

    openstack endpoint create --region RegionOne \
    --publicurl http://127.0.0.1:8386/v1.1/%\(project_id\)s \
    --adminurl http://127.0.0.1:8386/v1.1/%\(project_id\)s \
    --internalurl http://127.0.0.1:8386/v1.1/%\(project_id\)s \
    data_processing_local
..

Then the endpoint name should be changed in ``sahara.py`` under the module of
`sahara-dashboard/sahara_dashboard/api/sahara.py. <https://git.openstack.org/cgit/openstack/sahara-dashboard/tree/sahara_dashboard/api/sahara.py>`_

.. sourcecode:: python

    # "type" of Sahara service registered in keystone
    SAHARA_SERVICE = 'data_processing_local'


3. Hiding health check info
---------------------------

Sahara UI panels normally contain some information about cluster health. If
the relevant functionality has been disabled in the Sahara service, then
operators may prefer to not have any references to health at all in the UI,
since there would not be any usable health information in that case.

The visibility of health check info can be toggled via the
``SAHARA_VERIFICATION_DISABLED`` parameter, whose default value is False,
meaning that the health check info will be visible.

Example:

.. sourcecode:: python

    SAHARA_VERIFICATION_DISABLED = True
..
