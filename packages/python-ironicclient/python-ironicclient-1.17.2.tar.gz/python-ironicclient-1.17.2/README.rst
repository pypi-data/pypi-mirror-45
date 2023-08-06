========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/python-ironicclient.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

Python bindings for the Ironic API
==================================

This is a client for the OpenStack `Ironic
<https://wiki.openstack.org/wiki/Ironic>`_ API. It provides a Python API (the
``ironicclient`` module) and a command-line interface (``ironic``).

Development takes place via the usual OpenStack processes as outlined in the
`developer guide <https://docs.openstack.org/infra/manual/developers.html>`_. The master
repository is on `git.openstack.org
<https://git.openstack.org/cgit/openstack/python-ironicclient>`_.

``python-ironicclient`` is licensed under the Apache License like the rest
of OpenStack.


.. contents:: Contents:
   :local:

Python API
----------

Quick-start Example::
    >>> from ironicclient import client
    >>>
    >>> kwargs = {'os_auth_token': '3bcc3d3a03f44e3d8377f9247b0ad155',
    >>>           'ironic_url': 'http://ironic.example.org:6385/'}
    >>> ironic = client.get_client(1, **kwargs)


Command-line API
----------------

This package will install the ``ironic`` command line interface that you
can use to interact with the ``ironic`` API.

In order to use the ``ironic`` CLI you'll need to provide your OpenStack
tenant, username, password and authentication endpoint. You can do this with
the ``--os-tenant-name``, ``--os-username``, ``--os-password`` and
``--os-auth-url`` parameters, though it may be easier to set them
as environment variables::

    $ export OS_PROJECT_NAME=project
    $ export OS_USERNAME=user
    $ export OS_PASSWORD=pass
    $ export OS_AUTH_URL=http://auth.example.com:5000/v2.0

To use a specific Ironic API endpoint::

    $ export IRONIC_URL=http://ironic.example.com:6385

An example of creating a basic node with the pxe_ipmitool driver::

    $ ironic node-create -d pxe_ipmitool

An example of creating a port on a node::

    $ ironic port-create -a AA:BB:CC:DD:EE:FF -n nodeUUID

An example of updating driver properties for a node::

    $ ironic node-update nodeUUID add driver_info/ipmi_address=<IPaddress>
    $ ironic node-update nodeUUID add driver_info/ipmi_username=<username>
    $ ironic node-update nodeUUID add driver_info/ipmi_password=<password>


For more information about the ``ironic`` command and the subcommands
available, run::

    $ ironic help

OpenStackClient Baremetal Plugin
--------------------------------

In order to use Baremetal Plugin the OpenStackClient should be installed::

    # pip install python-openstackclient

An example of creating a basic node with the agent_ipmitool driver::

    $ openstack baremetal node create --driver agent_ipmitool

An example of creating a port on a node::

    $ openstack baremetal port create --node <UUID> AA:BB:CC:DD:EE:FF

An example of updating driver properties for a node::

    $ openstack baremetal node set --driver-info ipmi_address=<IPaddress> <UUID or name>

For more information about the ``openstack baremetal`` command and
the subcommands available, run::

    $ openstack help baremetal

* License: Apache License, Version 2.0
* Documentation: https://docs.openstack.org/python-ironicclient/latest/
* Source: https://git.openstack.org/cgit/openstack/python-ironicclient
* Bugs: https://bugs.launchpad.net/python-ironicclient

Change logs with information about specific versions (or tags) are
available at:

    `<https://git.openstack.org/cgit/openstack/python-ironicclient/>`_.
