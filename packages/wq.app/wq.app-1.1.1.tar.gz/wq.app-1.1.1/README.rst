|wq.app|

`wq.app <https://wq.io/wq.app>`__ is a suite of Javascript modules and
related assets, created to facilitate the rapid deployment of
offline-cabable HTML5 mobile and desktop data collection apps for
**crowdsourcing**, **citizen science**, and **volunteered geographic
information**, as well as professional **field data collection**. wq.app
is the client component of the `wq framework <https://wq.io>`__, and can
be used with any REST service as a backend. In particular, when combined
with a Mustache-capable REST service like
`wq.db <https://wq.io/wq.db>`__, wq.app can be used to create
**responsive, progressively enhanced** websites / apps, that can
selectively render individual application screens `on the server or on
the client <https://wq.io/docs/templates>`__ depending on project needs,
network connectivity, and offline storage availability.

|Latest PyPI Release| |Release Notes| |Documentation| |License| |GitHub
Stars| |GitHub Forks| |GitHub Issues|

|Travis Build Status|

Getting Started
---------------

.. code:: bash

    # Recommended: create virtual environment
    # python3 -m venv venv
    # . venv/bin/activate

    # Install entire wq suite (recommended)
    pip install wq

    # Install only wq.app
    pip install wq.app

See `the documentation <https://wq.io/docs/setup>`__ for more
information.

Features
--------

wq.app's `JavaScript modules <https://wq.io/docs/app>`__ are built on `a
number of libraries <https://wq.io/docs/third-party>`__ including
`RequireJS <http://requirejs.org>`__, `jQuery
Mobile <http://jquerymobile.com>`__, `Leaflet <http://leafletjs.com>`__,
`d3 <http://d3js.org>`__, and
`Mustache.js <https://mustache.github.com/>`__. wq.app extends these
libraries with:

-  `wq/app.js <https://wq.io/docs/app-js>`__, a high-level application
   controller and configuration-driven CRUD client (optimized for use
   with `wq.db.rest <https://wq.io/docs/about-rest>`__)
-  `wq/chart.js <https://wq.io/docs/chart-js>`__, configurable d3-based
   reusable charts, including time series and boxplots
-  `wq/map.js <https://wq.io/docs/map-js>`__, Leaflet integration for
   **wq/app.js** pages that contain geometry (loaded via GeoJSON)
-  `wq/model.js <https://wq.io/docs/model-js>`__, a lightweight
   implementation of models / collections
-  `wq/outbox.js <https://wq.io/docs/outbox-js>`__, an offline queue of
   ``<form>`` submissions for later synchronization
-  and a number of `other useful utilities <https://wq.io/docs/app>`__

To facilitate compact deployment, wq.app provides a Python-based `build
process <https://wq.io/docs/build>`__ for compiling wq apps: inlining
templates, optimizing code (via
`r.js <https://github.com/jrburke/r.js>`__), and generating a native
application package (via `PhoneGap
Build <https://build.phonegap.com/>`__). wq.app also includes
`jquery-mobile.scss <https://wq.io/docs/jquery-mobile-scss-themes>`__, a
SASS/SCSS stylesheet for generating custom jQuery Mobile themes.

.. |wq.app| image:: https://raw.github.com/wq/wq/master/images/256/wq.app.png
   :target: https://wq.io/wq.app
.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/wq.app.svg
   :target: https://pypi.org/project/wq.app
.. |Release Notes| image:: https://img.shields.io/github/release/wq/wq.app.svg
   :target: https://github.com/wq/wq.app/releases
.. |Documentation| image:: https://img.shields.io/badge/Docs-1.0-blue.svg
   :target: https://wq.io/wq.app
.. |License| image:: https://img.shields.io/pypi/l/wq.app.svg
   :target: https://wq.io/license
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/wq.app.svg
   :target: https://github.com/wq/wq.app/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/wq.app.svg
   :target: https://github.com/wq/wq.app/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/wq.app.svg
   :target: https://github.com/wq/wq.app/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/wq.app/master.svg
   :target: https://travis-ci.org/wq/wq.app
