REST API Version History
========================

This documents the changes made to the REST API with every
microversion change. The description for each version should be a
verbose one which has enough information to be suitable for use in
user documentation.

1.1
---

  This is the initial version of the v1.1 API which supports
  microversions. The v1.1 API is from the REST API users's point of
  view exactly the same as v1.0 except with strong input validation.

  A user can specify a header in the API request::

    OpenStack-API-Version: <version>

  where ``<version>`` is any valid api version for this API.

  If no version is specified then the API will behave as if a version
  request of v1.1 was requested.

1.2
---

  Add a new attribute 'nets' to the request to create a container.
  Users can use this attribute to specify one or multiple networks for
  the container. Each network could specify the neutron network, neutron
  port, or a v4/v6 IP address. For examples:

    [{'port': '1234567'}]
    [{'v4-fixed-ip': '127.0.0.1'}]
    [{'network': 'test'}]
    [{'network': 'test2'}]
    [{'v6-fixed-ip': '2f:33:45'}]

1.3
---

  Add 'auto_remove' field for creating a container.
  With this field, the container will be automatically removed if it exists.
  The new one will be created instead.

1.4
---

  Add host list api.
  Users can use this api to list all the zun compute hosts.
  Add get host api
  Users can use this api to get details of a zun compute host.
