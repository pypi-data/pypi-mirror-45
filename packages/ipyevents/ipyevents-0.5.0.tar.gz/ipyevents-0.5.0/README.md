ipyevents
=========
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mwcraig/ipyevents/master?filepath=doc%2FWidget%20DOM%20Events.ipynb)

*ipyevents* provides a custom widget for returning mouse and keyboard events to
Python. Use it to:

 - add keyboard shortcuts to an existing widget;
 - react to the user clicking on an image;
 - install callbacks on arbitrary mouse and keyboard events.

See [this demo notebook](doc/Widget%20DOM%20Events.ipynb) for documentation.

Installation
------------

To install using `conda`:

```bash
$ conda install -c conda-forge ipyevents
```

To install use `pip`:

    $ pip install ipyevents
    $ jupyter nbextension enable --py --sys-prefix ipyevents

To install with JupyterLab (whether you installed with `conda` or `pip`):

```bash
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager ipyevents
```

For a development installation (requires npm),

```bash
$ git clone https://github.com/mwcraig/ipyevents.git
$ cd ipyevents
$ pip install -e .
$ jupyter nbextension install --py --symlink --sys-prefix ipyevents
$ jupyter nbextension enable --py --sys-prefix ipyevents
```

For Jupyter Lab also do this:

```bash
$ cd js
$ npm install
$ npm run build
$ jupyter labextension install
```

