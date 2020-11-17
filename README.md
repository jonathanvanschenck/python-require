# python-require (repyrer)
Provides nodejs-style requiring of modules for python


This module allows imports of python modules using syntax similar to the node.js `require`
function. In particular, it takes string arguments comprised of (optionally) a
UNIX-style directory path and a module name, and returns a reference to the
loaded module. Specifying no directory path will have the module import
attempted first in the current working directory, then on the python path
variable (`sys.path`), allowing both local-to-the-folder imports and standard
library imports (as well as anything else you've configured into `sys.path`).
If an (absolute) directory path is included (i.e. a leading `/` in the directory path),
the module will first be attempted to be loaded from that directory first,
then the rest of the `sys.path` as a fallback. If a relative directory path
is provided (like `lib/module_name` or `../other_lib/module_name`) the current
working directory is used to resolve the relative path.

NOTE: the leading `./` characters on a directory path (as in
`./lib/module_name`) indicate that the directory path should be resolved
relative to the current file NOT the current working directory. For example,
suppose you have the following file structure:

```
top_folder
|-----main.py
|-----lib
  |-----A.py
  |-----sub_lib
    |-----B.py
```

Suppose `main.py` imports `A.py` as a module, and `A.py` in tern imports `B.py`
as a module. Inside of `A.py`, it should use `B = repyre('./sublib/B')`,
NOT `B = repyre('sublib/B')` since the latter will fail when `main.py`
imports `A.py` (because the current working directory will be `top_folder`
NOT `lib`). However, `main.py` is free to import `A.py` as `A = repyre('lib/A')`
or `A = repyre('./lib/A')` provided `main.py` will only ever be run directly
as a script from `top_folder`.


# Example Usage
You can use `repyrer` exactly as you would `import` to access the standard library,
and anything else you might have `pip` installed:

```python
>>> from repyrer import repyre
>>> os = repyre('os') # import standard library
>>> np = repyre('numpy') # import other libraries installed with pip, etc.
>>> plt = repyre('matplotlib.pyplot') # import sub-modules using '.' notation
```

You can also specify a directory path (relative to the current working directory, or absolute)
preceding the module name to access local libraries, suppose you have a file structure like:

```
folder
|----CWD
  |----main.py
  |----adjacent_file.py
  |----my_dev_lib
    |-----module_A.py
|----my_other_lib
  |-----module_B.py
```
Then, in the python shell
```python
>>> adjacent = repyre('adjacent_file') # import other files relative to the CWD
>>> A = repyre('my_dev_lib/module_A') # import modules from a relative directory path (relative to CWD)
>>> B = repyre('../my_other_lib/module_B') # can use '..' in directory paths
```

And in a script like `main.py`:
```python
from repyrer import repyre

adjacent = repyre('adjacent_file') # only works if script is run in this folder
adjacent = repyre('./adjacent_file') # safe to run from anywhere
```
