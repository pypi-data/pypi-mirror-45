
# docsbackup

   This tool can take a list of URLs to google documents and saves them with a
   timestamp. It can be used to include shared documents in backups and/or
   extract reference versions at specific points in time.
   The list of URLs can be provided in different formats or can be extracted by
   scanning through documents. The extraction is based on a prior conversion 
   with [Pandoc](http://pandoc.org).


# Install

   The fastest way to install docsbackup is to use your systems tools:

    pip install docsbackup

   To use the latest test version check out the test.pypi server:

    pip install --index-url https://test.pypi.org/simple docsbackup


## Requirements

   All required packages are listed in `environment.yaml`. In case you
   installed docsbackup via a package management system like pip, anaconda,
   miniconda, ... all dependencies should already be installed automatically.


# Getting Started

   After installation run `docsbackup --help` to get a first overview of
   command line options and usage.


## Further reading

   For details about the used tools and formats following links may provide
   more details.

   * [Pandoc](http://pandoc.org/)
   * [YAML specification](http://yaml.org/spec/)) and the
     [ruamel.yaml](https://yaml.readthedocs.io/en/latest/basicuse.html)
     package.


# Developing docsbackup

   Contributions are very welcome! Write issues for feature requests or
   directly file a pull-request with your contribution and/or contact me
   directly!


## Tests

   This project uses the [PyTest framework](https://docs.pytest.org/en/latest/)
   with tests defined in the [tests/](tests/) sudirectory. It is added into the
   setuptools config, so that it can be run with

    python setup.py test

   This automatically tests a temporarily packaged version.

   Alternatively you can run `pytest` manually with all it [glory
   details](https://docs.pytest.org/en/latest/usage.html).


## Releases

   The release workflow is mostly automated and is in the [release/](release/)
   folder.


