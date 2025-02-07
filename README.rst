.. image:: https://github.com/gdoumenc/coworks/raw/dev/docs/img/coworks.png
    :height: 80px
    :alt: CoWorks Logo

|Maintenance| |Build Status| |Documentation Status| |Coverage| |Python versions| |Licence|

.. |Maintenance| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=plastic
    :alt: Maintenance
.. |Build Status| image:: https://img.shields.io/travis/com/gdoumenc/coworks?style=plastic
    :alt: Build Status
.. |Documentation Status| image:: https://readthedocs.org/projects/coworks/badge/?version=master&style=plastic
    :alt: Documentation Status
.. |Coverage| image:: https://img.shields.io/codecov/c/github/gdoumenc/coworks?style=plastic
    :alt: Codecov
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/coworks?style=plastic
    :alt: Python Versions
.. |Licence| image:: https://img.shields.io/github/license/gdoumenc/coworks?style=plastic
    :alt: Licence

CoWorks is a unified serverless microservices framework based on AWS technologies
(`API Gateway <https://aws.amazon.com/api-gateway/>`_, `AWS Lambda <https://aws.amazon.com/lambda/>`_),
the `Flask <https://github.com/pallets/flask>`_ framework and the `Airflow <https://github.com/apache/airflow>`_
plateform.

The aim of this project, is to offer a very simplified experience of microservices. For such purpose, we divided the
CoWorks framework in two levels.

The first one is made of atomic microservices (``TechMicroservice``) each composed of simple python
`Flask <https://github.com/pallets/flask>`_ application and deployed as serverless Lambda.
Those technical microservice may be can be called synchronously or asynchronously.

The second level is made of composed business microservices (``BizMicroservice``) which are
`Airflow <https://github.com/apache/airflow>`_ dags providing orchestration of technical microservices.

You can get a quickstart on `TechMicroService <https://coworks.readthedocs.io/en/latest/tech_quickstart.html>`_ then
continue with `BizMicroService <https://coworks.readthedocs.io/en/latest/biz_quickstart.html>`_


Documentation
-------------

* Get started: `Installation <https://coworks.readthedocs.io/en/latest/installation.html/>`_
* Complete reference guide: `Documentation <https://coworks.readthedocs.io/>`_.
* Read `FAQ <https://coworks.readthedocs.io/en/latest/faq.html/>`_ for other informations.


Contributing
------------

We work hard to provide a high-quality and useful framework, and we greatly value
feedback and contributions from our community. Whether it's a new feature,
correction, or additional documentation, we welcome your pull requests. Please
submit any `issues <https://github.com/aws/coworks/issues>`__
or `pull requests <https://github.com/aws/coworks/pulls>`__ through GitHub.

Related Projects
----------------

* `Flask <https://github.com/pallets/flask>`_ - Lightweight WSGI web application framework (`Donate to Pallets <https://palletsprojects.com/donate>`_).
* `Click <https://github.com/pallets/click>`_ -  A package for creating beautiful command line interfaces.
* `Airflow <https://github.com/apache/airflow>`_ A platform to programmatically author, schedule, and monitor workflows.
* `Terraform <https://github.com/hashicorp/terraform>`_ - Infrastructure configuration management tool.


