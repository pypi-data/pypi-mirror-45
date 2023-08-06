============================
Usage and Quick Start Guides
============================

KloudBuster User Interfaces
---------------------------
KloudBuster provides 3 interfaces, the easiest being the **Web User Interface**.
It offers the most user friendly interface and needs the least learning to get
started. **CLI** is the traditional way to run applications. It has the most
comprehensive feature sets when compared to the other methods. **REST API**
gives another way to access and control KloudBuster from another application.

The Web UI is fully implemented on top of the REST API.

OpenStack Cloud Pre-Requisites
------------------------------
OpenStack cloud pre-requisites to run KloudBuster:

    * Neutron networking
    * Admin access to the cloud under test (non-admin might work with some
      tweaks and limitations)
    * 3 available floating IPs if running the HTTP data plane scale test
    * 2 available floating IPs if running the Storage scale test

KloudBuster Installation Options
--------------------------------

There are 4 different ways to install KloudBuster:

- use a pre-built Docker container (recommended)
- use a pre-built VM image (if you prefer to run the KloudBuster application in a VM and do not need CLI)
- install from PyPI (if you prefer to use pip install)
- install directly from GitHub (git clone, for code development or if you want to browse the code)

Users of KloudBuster who prefer to use the CLI or who prefer to run KloudBuster
locally on their workstation or laptop can use the PyPI based installation
(pip install) or the Docker container.

Docker container, Web Service and PyPI based installation will satisfy most use cases
and are the recommended ways for running KloudBuster under production environments
or through an automated or scheduled job.


Quick Start Guides
------------------
.. toctree::
   :maxdepth: 2

   quickstart_docker
   quickstart_pip
   quickstart_vmapp
   quickstart_git

.. _webui_usage:

Using the KloudBuster Web UI
----------------------------

Using any browser, point to the provided URL. You will get a Login page where
you will need to enter:

   * The type of scale test (HTTP data plane or storage)
   * The location of the openrc file for the cloud under test and the corresponding
     OpenStack password

You could modify the scale test configuration options or simply start the scale
test with the default scale configuration. Click on Stage button to instruct
KloudBuster to stage all the OpenStack resources. This can take time depending
on how many VMs are requested and how fast is the cloud under test.

Once staging is done, click on the Run button to run the scale test.

.. _rest_usage:

Interacting with the KloudBuster REST Interface
-----------------------------------------------

REST Documentation
^^^^^^^^^^^^^^^^^^

Once the server is started, you can use different HTTP methods
(GET/PUT/POST/DELETE) to interact with the KloudBuster REST interface using the
provided URL at port 8080.

    * `KloudBuster REST API Documentation Preview <https://htmlpreview.github.io/?https://opendev.org/x/kloudbuster/src/branch/master/doc/source/_static/kloudbuster-swagger.html>`_
    * `REST API Documentation (Swagger yaml) <https://opendev.org/x/kloudbuster/src/branch/master/doc/source/_static/kloudbuster-swagger.html>`_


The following curl examples assume the server runs on localhost.

Display version and retrieve default configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To get the current version and retrieve the default configuration and copy to a file:

.. code-block:: bash

    > curl http://localhost:8080/api/kloudbuster/version
    7.1.1
    > curl http://localhost:8080/api/config/default_config >default_config

     ...


Create a new Kloudbuster session
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before running any benchmark, the first step is to create a new session:

The body of the REST request msut have the following fields:

.. code-block:: bash

    {
       'credentials': {'tested-rc': '<STRING>',
                       'testing-rc': '<STRING>'},
       'kb_cfg': {<USER_OVERRIDED_CONFIGS>},
       'topo_cfg': {<TOPOLOGY_CONFIGS>},
       'tenants_cfg': {<TENANT_AND_USER_LISTS_FOR_REUSING>},
       'storage_mode': true|false
    }

List of fields and content:

- credentials (mandatory)
- tested-rc (mandatory) contains the openrc variables (string containing the list of variables separated by \n)
- testing-rc (optional) only needed in case of dual cloud testing (HTTP only)
- kb_cfg (mandatory) a string containing the Kloudbuster configuration to use (json)
- topo_cfg (optional) a string containing the topology configuration (json)
- tenants_cfg (optional) a string containing the list of tenants and users to use (json)
- storage_mode (mandatory) true for storage benchmark, false for HTTP benchmark


Example of configuration:

.. code-block:: bash

    # Content of a standard openrc file that we store in a variable
    OPENRC="export OS_CACERT=/root/openstack-configs/haproxy-ca.crt
    export OS_AUTH_URL=https://10.0.0.1:5000/v3
    export OS_USERNAME=admin
    export OS_PASSWORD=55DgmREFWenMqkxK
    export OS_REGION_NAME=RegionOne
    export OS_PROJECT_NAME=admin
    export OS_PROJECT_DOMAIN_NAME=default
    export OS_USER_DOMAIN_NAME=default
    export OS_IDENTITY_API_VERSION=3"

    # Example of simple Kloudbuster configuration
    KBCFG="{client:{storage_stage_configs:{ vm_count: 1, disk_size: 50, io_file_size: 1},
    storage_tool_configs:{[description: 'Random Read', mode: 'randread', runtime: 30,
    block_size: '4k', iodepth: 4]}}}"

    # REST request body in json format
    BODY="{'credentials': {'tested-rc': $OPENRC},
           'kb_cfg': $KBCFG,
           'storage_mode': true}"

Create the Kloudbuster session with above configuration:

.. code-block:: bash

    > curl -H "Content-Type: application/json" -X POST -d "$BODY" http://localhost:8080/api/config/running_config

Note that this request only updates the running configuration and does not start any benchmark.
It will return a session ID that needs to be passed to subsequent REST requests.

Start a storage benchmark using the running configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SESSION_ID is the id returned from the /api/config/running_config POST request.

.. code-block:: bash

    > curl -H "Content-Type: application/json" -X POST http://localhost:8080/api/kloudbuster/run_test/$SESSION_ID


.. _upload_kb_image:

Get the KloudBuster VM Image
----------------------------

KloudBuster needs one "universal" test VM image
(referred to as "KloudBuster image") that contains the necessary test software.
The KloudBuster image is then instantiated by the KloudBuster application in
potentially large number of VMs using the appropriate role (HTTP server, HTTP
traffic generator...).
Upload of the VM image to OpenStack is automatic with the KloudBuster container (as the VM image is
included in the container itself). For non container usages, it requires building a VM image or obtaining
it from the Internet (see below).

.. note::

   The same KloudBuster VM image can be instantiated for running the test functions
   (HTTP servers, HTTP traffic generators, file access tools) and for running KloudBuster as a web service.

Extract the KloudBuster VM image to the local directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This requires Docker to be installed and requires Internet access to DockerHub.

Use the kb_extract_img_from_socker.sh script to download a copy of the VM image from DockerHub.
By default the script will download the VM image with the same version as the installed
KloudBuster package.

.. code-block:: bash

   kb_extract_img_from_socker.sh

Once extracted, you can let KloudBuster upload the VM image for you on a subsequent run (simplest and recommended) or the VM image can be manually uploaded to OpenStack using Horizon or the glance API.
KloudBuster by default will look into the root of the KloudBuster package or into the current directory to
check if the VM image file is present, and automatically upload it if it is not already in OpenStack.


Upload the KloudBuster VM image using the Horizon Dashboard (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the dashboard, create a new image and select "Image File" and select the VM image file.

The name of the image in Glance *must* match exactly the image name (without the .qcow2 extension, e.g. "kloudbuster-7.0.0").

Upload the KloudBuster VM image using the Glance CLI (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This assumes that you have installed the OpenStack Glance API and have sourced
the appropriate openrc file.

To upload the image from a local copy of that image using the Glance CLI:

.. code-block:: bash

    glance image-create --file kloudbuster-7.0.0.qcow2 --disk-format qcow2 --container-format bare --visibility public --name kloudbuster-7.0.0
