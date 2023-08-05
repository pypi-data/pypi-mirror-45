.. highlight:: sh

Installation
============

The recommended way to install `ligo.skymap` is using `pip
<https://pip.pypa.io>`_, which will also automatically install all of the
required Python packages listed below. On Linux and macOS systems, this method
will install pre-built binaries from the `Python package index
<https://pypi.org/project/ligo.skymap/>`_. (On other operating systems you can
:doc:`install from source <../develop>`.)

Basic Requirements
------------------

*  `Python <https://www.python.org>`_ ≥ 3.6
*  `pip <https://pip.pypa.io>`_

Required Python Dependencies
----------------------------

When you use pip to install `ligo.skymap` with pip, it will automatically
install the following required Python packages:

*  `Astroplan <http://astroplan.readthedocs.io>`_
*  Astropy_ ≥ 3.1
*  `astropy-healpix <https://astropy-healpix.readthedocs.io>`_
*  `Healpy <http://healpy.readthedocs.io>`_
*  `h5py <https://www.h5py.org>`_
*  `LALSuite <https://pypi.python.org/pypi/lalsuite>`_
*  `lscsoft-glue <https://pypi.org/project/lscsoft-glue/>`_
*  `ligo-gracedb <https://pypi.org/project/ligo-gracedb/>`_
*  `ligo-segments <https://pypi.org/project/ligo-segments/>`_
*  `Matplotlib <https://matplotlib.org>`_ ≥ 2.1.0
*  `NetworkX <https://networkx.github.io>`_
*  `Numpy <http://www.numpy.org>`_ ≥ 1.14
*  `Pillow <http://pillow.readthedocs.io>`_ ≥ 2.5.0
*  `ptemcee <https://github.com/willvousden/ptemcee>`_
*  `python-ligo-lw <https://pypi.org/project/python-ligo-lw/>`_
*  `Reproject <https://reproject.readthedocs.io>`_ ≥ 0.3.2
*  `Scipy <https://www.scipy.org>`_ ≥ 0.14
*  `Seaborn <https://seaborn.pydata.org>`_ ≥ 0.8.0
*  `tqdm <https://tqdm.github.io>`_
*  `pytz <http://pytz.sourceforge.net>`_

Optional Python Dependencies
----------------------------

The following packages are optional for specific features:

*  `pytest <https://docs.pytest.org>`_ for running the test suite

Quick Start
-----------

Just run this command::

    $ pip install ligo.skymap
