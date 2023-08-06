=======
taggedartifacts
=======


.. image:: https://img.shields.io/pypi/v/taggedartifacts.svg
        :target: https://pypi.python.org/pypi/taggedartifacts

.. image:: https://circleci.com/gh/jisantuc/taggedartifacts.svg?style=svg
    :target: https://circleci.com/gh/jisantuc/taggedartifacts

.. image:: https://pyup.io/repos/github/jisantuc/taggedartifacts/shield.svg
     :target: https://pyup.io/repos/github/jisantuc/taggedartifacts/
     :alt: Updates



Simple artifact versioning and caching for scientific workflows


* Free software: MIT license
* Documentation: https://taggedartifacts.readthedocs.io.


Features
--------

:code:`taggedartifacts` exists to provide a simple interface for versioning functions that produce artifacts.
An "artifact" could be anything -- maybe you have some sort of ETL pipeline that writes intermediate files,
or you have a plotting function that writes a bunch of plots to disk, or you have a machine learning
workflow that produces a bunch of model files somewhere. The purpose of :code:`taggedartifacts` is to allow you
to write normally -- give your output its regular name, like :code:`plot.png` -- and automatically attach
git commit and configuration information as part of the path.

Example
-------

The following example shows how to use :code:`taggedartifacts` to tag an output file with commit and config info:

.. codeblock:: python

    from taggedartifacts import Artifact
    @Artifact(keyword='outpath', config={}, allow_dirty=True)
    def save_thing(outpath):
        with open(outpath, 'w') as outf:
            outf.write('good job')
    

    save_thing(outpath='foo.txt')

The resulting file that would be created would be :code:`foo-<commit>-<config-hash>.txt`, without having to
litter string formats and fetching git commit info throughout the code.

Why
---

It's really easy, once you start running a lot of experiments, to end up with a ton of output files
produced at different times with names like :code:`plot.png`, :code:`plot2.png`, :code:`plot-please-work.png`, etc.
Later, you'll maybe want to show someone a plot, and they'll try to reproduce it, and you won't be
able to tell them the state of the code when the plot was produced. That's not great! :code:`taggedartifacts`
offers one solution to this problem, where you can tell at a glance whether two files were produced
by the same code and the same configuration.

Isn't this just another workflow library
----------------------------------------

It's not! I promise.

The workflow library ecosystem in python already has a lot of entrants, like Luigi_, Airflow_, 
Pinball_, and probably many I haven't heard of. There are also experiment and data/code versioning systems
around like DVC_, and older solutions to DAGs that understand how not to redo work, like :code:`make`. :code:`taggedartifacts`
isn't really like any of those. It isn't aware of a DAG of all of your tasks at any point, and it doesn't
know anything about data science workflows in general. It only knows about tagging some sort of file-based
output with git commit and configuration information so that you can tell whether two artifacts produced
potentially on different computers should match.

As a result, you don't have to have a separate daemon running, you don't get anything like task
distribution and parallelization for free, and you don't get a special CLI. :code:`taggedartifacts` only attempts to
solve one problem.

.. _Luigi: https://github.com/spotify/luigi
.. _Airflow: https://github.com/apache/airflow
.. _Pinball: https://github.com/pinterest/pinball
.. _DVC: https://github.com/iterative/dvc

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
