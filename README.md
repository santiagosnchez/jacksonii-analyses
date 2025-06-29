# *Amanita jacksonii* variant analysis

This repo includes scripts, workflows, and environments for analyzing population genomic data in *Amanita jacksonii* species complex --an ectomycorrhizal basidiomycete in the genus *Agaricales*.

## Load the Python toolkit environment

Use [Poetry](https://python-poetry.org/) to create and load the Python environment for all the code to properly work.

You will need to use **Python3.12** or higher. If you don't have poetry already installed, use `pip` to install it.

```bash
python3 -m pip install poetry
```

Once you have `poetry` up and running, install all the required packages:

```bash
poetry install
```

By default, Poetry creates a virtual environment in your local cache directory (usually `$HOME/.cache`). To load this environment onto your Bash shell run:

```bash
$(poetry env activate)
```

You'll probably see something like `(jacksonii-analyses-py3.12)` in your shell prompt.

This means your shell is active and you can start using the tools. For example, you can try this on a python shell:

```python
from jacksonii_analyses import vcf_parser
```

If you get an error, it means the env was not loaded. If the module loads without error, you should be good to go.

## Deactivating the environment

```bash
deactivate
```

This should take you back to your default shell.

## Running Jupyter notebooks (on the proper environment)

Making Jupyter pickup/see the right environment might be tricky. These are some steps I took to make it work.

### Register the ipykernel locally

After loading the environment, register the ipython kernel:

```bash
$(poetry env activate) && \
python -m ipykernel install --user --name=jacksonii --display-name="Python (jacksonii)"
```

The python path should point to some location in the actual virtual environment. For example:

```bash
which python3
# $HOME/.cache/pypoetry/virtualenvs/jacksonii-analyses-xxxxxxx-py3.12/bin/python3
```

### In VS Code

For this to work in VS Code you need to witch the python flavor at the bottom right part of your workspace. If you don't see it, just open a python script in VS Code and click on the python interpreter version. Copy and paste the full path to the python used in your virtual environment. Something like:

```bash
$HOME/.cache/pypoetry/virtualenvs/jacksonii-analyses-xxxxxxx-py3.12/bin/python3
```

You should now be able to select the Python from the virtual environment when opening the jupyter notebook.

