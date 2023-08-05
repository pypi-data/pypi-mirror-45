paws: the Platform for Automated Workflows by SSRL 
==================================================


Introduction
------------

`paws` stands for the Platform for Automated Workflows by SSRL.
It was conceived to serve as a lean and modular
workflow manager for scientific data.

`paws` interfaces with an ever-growing number of packages 
and provides for users to add their own Operations,
by writing isolated Python modules following a simple template.

The essential ingredients of `paws` are Operations, Workflows, and Plugins.
A `paws` Operation is meant to take some inputs and produce some outputs-
it is essentially  a function, wrapped in a class, wrapped in a Python module.
The class and module layers are used for certain conveniences 
in the implementation of `paws` Workflows.
A `paws` Plugin is an object that should persist over time
to repeatedly execute one or more activities,
for example to monitor an experimental apparatus,
or to expose functionalities of a complex object for Operations to use.
A `paws` Workflow contains the logic necessary for stitching together Operations and Plugins,
and despite the distinction in name, it implements the same interface as an Operation.

Disclaimer: `paws` is neither the first nor the most sophisticated
way to build and manage data processing workflows.
Its development was driven by a need
for modularity and extensibility,
for rapid development and deployment 
of stand-alone applications for a wide variety of experimental control
and data processing tasks.


Documentation
-------------

The documentation for `paws` is hosted by readthedocs.org:
`http://paws.readthedocs.io/en/latest/`.
This documentation is continually under development.
Please contact the developers at `paws-developers@slac.stanford.edu`
if the documentation fails to answer your questions.


API Examples
------------

The following are examples that explore 
the capabilities of the `paws` API.

TODO: write new examples


Installation
------------

NOTE: all deployments are currently outdated or under heavy development.
Please contact the development team if you are interested in this package.

`paws` is available on PyPI and Anaconda.
Deployments to PyPI are performed regularly.
Currently, we only deploy relatively stable versions to Anaconda.

To install from PyPI, invoke `pip`:
`pip install pypaws`.

To install from Anaconda, use `conda`:
`conda install -c ssrl-paws pypaws` 

All of the dependencies of the `paws` Operations 
are not necessarily declared as dependencies of `paws`.
This keeps the Python environment relatively lean
and avoids obnoxious installation overhead,
but it means that users will have to prepare their
environments for the Operations they want to use.

The documentation of `paws` includes instructions
for installing the dependencies of each Operation.
NOTE: this is currently false. 


Attribution
-----------

`paws` was written at SSRL by Chris Tassone's research group.
If you use `paws` in your published research, 
a citation would be appreciated.

Before citing `paws`, it is of primary importance that you cite 
the authors of the original work that produced your results: 
this is almost certainly separate from the authors of `paws`.
Citations for your specific Operations should be found
in the `paws` documentation.
If you have trouble finding proper citations,
please contact us at `paws-developers@slac.stanford.edu`,
and we will do our best to help.


Contribution
------------

Contribution to `paws` is encouraged and appreciated.
Get in touch with the `paws` development team
at `paws-developers@slac.stanford.edu`.
If you are able to develop without assistance,
feel free to submit a pull request against the `dev` branch at
https://github.com/slaclab/paws.


License
-------

The 3-clause BSD-like license attached to this software 
can be found in the LICENSE file in the source code root directory.

