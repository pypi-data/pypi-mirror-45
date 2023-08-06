# pprofile_ext
IPython extension for the pprofile line-profiler. The extension allows a user to mark a line or cell 
of an IPython notebook and run the [pprofile](https://github.com/vpelletier/pprofile) performance profiler
on the marked section of code. The result of the profile run will be written to HTML and can be viewed in
any browser. If the extension is used from within an IPython notebook then the results are displayed inline
in the notebook.

## Installation

The `pprofile_ext` ipython extension canbe installed using pip:

```bash
pip install pprofile_ext
```

## Usage
To load the extension from the IPython REPL or in a notebook cell type and execute

```python
%load_ext pprofile_ext
```

To view the pprofile_ext help type `%pprofile?`, which will display

<pre>
%pprofile [-n NAME] [-w WIDTH] [-h HEIGHT] [code [code ...]]

PProfile IPython extension

positional arguments:
  code

optional arguments:
  -n NAME, --name NAME  Name of the directory relative to the current notebook
                        in which to store the profile output and the html
                        version of the profile output; If the directory does
                        not exist it will be created. If the directory does
                        exist a new directory will be created that has a
                        running integer suffix _x. The default name is
                        pprofile_output.
  -w WIDTH, --width WIDTH
                        Width in pixels of the iframe displaying the pprofile
                        output; default 980 (used only in cell mode)
  -h HEIGHT, --height HEIGHT
                        Height in pixels of the iframe displaying the pprofile
                        output; default 400 (used only in cell mode)
</pre>

