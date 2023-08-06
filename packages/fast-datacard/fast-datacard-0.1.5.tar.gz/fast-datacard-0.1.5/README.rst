=====================
fast-datacard
=====================


.. image:: https://img.shields.io/pypi/v/fast-datacard.svg
        :target: https://pypi.python.org/pypi/fast-datacard


.. image:: https://readthedocs.org/projects/fast-datacard/badge/?version=latest
        :target: https://fast-datacard.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


* Free software: Apache Software License 2.0
* Documentation: https://fast-datacard.readthedocs.io.

Overview
--------
fast-datacard is a python packaged developed within the `Faster Analysis Software Taskforce (FAST)`_ collaboration.
The main purpose of this package is to create datacards_ compatible with the `HiggsCombine tool`_ from data frames.
The package will take categorical\ :sup:`citation needed` data frames, e.g. as created by the alphatwirl_ package, and create
the necessary ROOT and datacard outputs.

Features
--------

* convert categorical data frames (see `examples/data/*.csv`) into valid data to use in the `HiggsCombine tool`_.

Usage
--------
The usage is the following:::

    fast_datacard <yaml_config_file>

An example `yaml` config file is available: ``examples/datacards_config.yaml``. The config file lists all the input event categories, regions, physics processes, dataframes, etc. A few things should be noted:

* The existence of the ``general``, ``regions``, ``signals``, ``backgrounds`` and ``systematics`` blocks is mandatory.
* ``analysis_name``, ``version``, and ``dataset`` are just used for versioning.
* The value of ``luminosity`` (float, in fb-1) is used to weight the signal and backgrounds ``content`` and ``error`` to the expected luminosity.
* For each signal and background process named ``X``, there should be a file in the ``path_to_dfs`` directory named ``X.csv`` (a whitespace-separated Pandas dataframe). 
* ``data_names_df`` should be equal to the ``process`` name used for data in the dataframe (``Data`` in the example config file) and also should be the name of the ``.csv`` dataframe in ``path_to_dfs``. ``data_names_dc`` will the name of the output data histogram and should be equal to ``data_obs`` as imposed by the `HiggsCombine tool`_.
* There has to be at least one signal and one background.
* Backgrounds (but not signals, see below) can live only in specific region(s) (see example config file).
* The systematics listed in the ``systematics`` block can have three types: ``lnN``, ``lnU``, and ``shape``. The first two are normalization uncertainties and a value should be provided that corresponds to 1 + X, where X is the uncertainty one sigma level in percent (see example config file). For the ``shape`` type, no value is required as the shape itself encodes the uncertainty level. There is no need to specify Up/Down in the name of the uncertainty as this will be derived from the input dataframe (see below).
* The systematics can apply only to a given set of signals and/or backgrounds, in which case the name of the process (identical to the one in the dataframe) should be specified. If the systematic applies to all backgrounds, ``backgrounds`` can be used instead of listing all the background processes (and the same is true for ``signals``).

The configuration for running is also partly derived from the input dataframes, which formats should therefore follow a few rules:

1. The columns should be named::

    process region category systematic variable variable_low variable_high content error

Where:

* ``process`` is the name of the physics process, e.g. ``VBF``, ``Ewk``, etc.
* ``region`` is the name of the region, e.g. ``Signal``, ``ControlRegion1``, etc.
* ``category`` is the name of the event category, e.g. ``2jet``, ``highMass``, etc. Each unique name will be considered as a different category.
* ``systematic`` is the name of systematic shape variation that is applied to obtain the ``content`` of this row. E.g. if a process is characterized by two shape systematic uncertainties named ``syst1`` and ``syst2``, then the dataframe should contain 5 variations: ``nominal``, ``syst1_Up``, ``syst1_Down``, ``syst2_Up``, ``syst2_Down`` for each bin where this process exists.
* ``variable`` is the name of variable that defines the x-values in the output histograms. It is not used by the code but is mainly there to keep track of the fit variables in different categories.
* ``variable_low`` and ``variable_high`` define the binning along x in the output histograms used for the fit. Each unique set of (``variable_low``, ``variable_high``) will be considered as a unique bin.
* ``content`` is the yield for this specific (``process``, ``region``, ``category``, ``systematic``, ``variable``, ``variable_low``, ``variable_high``) bin.
* ``error`` is the error assigned to the yield (please note it is not the square of the error! therefore for a Poisson experiment it should be sqrt(N).)

The use of ``region`` or ``category`` is optional in the sense that an analysis might contain only one region and one category; in this case, the value of each column needs to be filled by the same value for all rows.

2. The signal(s) process(es) should be defined in all categories and regions, even if the ``content`` is 0. In other words, if you're looking for an exotics signal named ``bananas``, the code assumes it will find a row with ``bananas`` 's ``content`` for *each* bin of the analysis (i.e. the code never makes the assumption that the signal cannot live in the control regions as well).

3. The ``data`` should be defined in all categories and regions, even if the ``content`` is 0. If data is not defined somewhere, the category/region shouldn't even exist in the analysis.

The package will produce two sets of outputs:

* Text datacards that summarize the physics processes, the yields, and meta-information about the analysis.
* ROOT datacards that contain histrograms describing shapes that will be used in the fit.

Both serve as inputs to the `HiggsCombine tool`_.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`HiggsCombine tool`: https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit
.. _`Faster Analysis Software Taskforce (FAST)`: https://fast-hep.web.cern.ch/fast-hep
.. _datacards: https://cms-hcomb.gitbooks.io/combine/content/part2/settinguptheanalysis.html#preparing-the-datacard
.. _alphatwirl: https://github.com/alphatwirl/alphatwirl
