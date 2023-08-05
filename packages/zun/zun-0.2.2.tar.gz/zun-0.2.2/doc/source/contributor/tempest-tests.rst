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

=========================
Run tempest tests locally
=========================

This is a guide for developers who want to run tempest tests in their local
machine.

Zun contains a suite of tempest tests in the zun/tests/tempest directory.
Tempest tests are primary for testing integration between Zun and its
depending software stack (i.e. Docker, other OpenStack services). Any proposed
code change will be automatically rejected by the gate if the change causes
tempest test failures. If this happens, contributors are suggested to refer
this document to re-run the tests locally and perform any necessary
trouble-shooting.

Prerequisite
============

You need to deploy Zun in a devstack environment.

Clone devstack::

    # Create a root directory for devstack if needed
    sudo mkdir -p /opt/stack
    sudo chown $USER /opt/stack

    git clone https://git.openstack.org/openstack-dev/devstack /opt/stack/devstack

We will run devstack with minimal local.conf settings required. You can use the
sample local.conf as a quick-start::

    git clone https://git.openstack.org/openstack/zun /opt/stack/zun
    cp /opt/stack/zun/devstack/local.conf.sample /opt/stack/devstack/local.conf

Run devstack::

    cd /opt/stack/devstack
    ./stack.sh

**NOTE:** This will take a while to setup the dev environment.

Run the test
============

Navigate to tempest directory::

    cd /opt/stack/tempest

Run this command::

    tox -eall-plugin -- zun.tests.tempest.api
