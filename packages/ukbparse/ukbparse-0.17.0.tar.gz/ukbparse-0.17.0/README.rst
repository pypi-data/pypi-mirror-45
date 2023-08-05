``ukbparse`` - the UK BioBank data parser
=========================================


.. image:: https://img.shields.io/pypi/v/ukbparse.svg
   :target: https://pypi.python.org/pypi/ukbparse/

.. image:: https://anaconda.org/conda-forge/ukbparse/badges/version.svg
   :target: https://anaconda.org/conda-forge/ukbparse

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1997626.svg
   :target: https://doi.org/10.5281/zenodo.1997626

.. image:: https://git.fmrib.ox.ac.uk/fsl/ukbparse/badges/master/coverage.svg
   :target: https://git.fmrib.ox.ac.uk/fsl/ukbparse/commits/master/


``ukbparse`` is a Python library for pre-processing of UK BioBank data.


    ``ukbparse`` is developed at the Wellcome Centre for Integrative
    Neuroimaging (WIN@FMRIB), University of Oxford. ``ukbparse`` is in no way
    endorsed, sanctioned, or validated by the :ref:`UK BioBank
    <https://www.ukbiobank.ac.uk/>`_.

    ``ukbparse`` comes bundled with metadata about the variables present in UK
    BioBank data sets. This metadata can be obtained from the :ref:`UK BioBank
    online data showcase <https://biobank.ctsu.ox.ac.uk/showcase/index.cgi>`_


Installation
------------


Install ``ukbparse`` via pip::


    pip install ukbparse


Or from ``conda-forge``::

    conda install -c conda-forge ukbparse


Comprehensive documentation does not yet exist.


Introductory notebook
---------------------


The ``ukbparse_demo`` command will start a Jupyter Notebook which introduces
the main features provided by ``ukbparse``. To run it, you need to install a
few additional dependencies::


    pip install ukbparse[demo]


You can then start the demo by running ``ukbparse_demo``.


.. note:: The introductory notebook uses ``bash``, so is unlikely to work on
          Windows.


Usage
-----


General usage is as follows::


    ukbparse [options] output.tsv input1.tsv input2.tsv


You can get information on all of the options by typing ``ukbparse --help``.


Options can be specified on the command line, and/or stored in a configuration
file. For example, the options in the following command line::


    ukbparse \
      --overwrite \
      --import_all \
      --log_file log.txt \
      --icd10_map_file icd_codes.tsv \
      --category 10 \
      --category 11 \
      output.tsv input1.tsv input2.tsv


Could be stored in a configuration file ``config.txt``::


    overwrite
    import_all
    log_file       log.txt
    icd10_map_file icd_codes.tsv
    category       10
    category       11


And then executed as follows::


    ukbparse -cfg config.txt output.tsv input1.tsv input2.tsv


Customising
-----------


``ukbparse`` contains a large number of built-in rules which have been
specifically written to pre-process UK BioBank data variables. These rules are
stored in the following files:


 * ``ukbparse/data/variables_*.tsv``: Cleaning rules for individual variables
 * ``ukbparse/data/datacodings_*.tsv``: Cleaning rules for data codings
 * ``ukbparse/data/types.tsv``: Cleaning rules for specific types
 * ``ukbparse/data/processing.tsv``: Processing steps


You can customise or replace these files as you see fit. You can also pass
your own versions of these files to ``ukbparse`` via the ``--variable_file``,
``--datacoding_file``, ``--type_file`` and ``--processing_file`` command-line
options respectively.``ukbparse`` will load all variable and datacoding files,
and merge them into a single table which contains the cleaning rules for each
variable.

Finally, you can use the ``--no_builtins`` option to bypass all of the
built-in cleaning and processing rules.


Tests
-----


To run the test suite, you need to install some additional dependencies::


      pip install ukbparse[test]


Then you can run the test suite using ``pytest``::

    pytest


Citing
------


If you would like to cite ``ukbparse``, please refer to its `Zenodo page
<https://doi.org/10.5281/zenodo.1997626>`_.
