import sys
import os
import re
from importlib import import_module

def repyre(path, force_reload = False):
    """Import a specified module

    This function imports python modules using syntax similar to the node.js `require`
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

    top_folder
    |-----main.py
    |-----lib
      |-----A.py
      |-----sub_lib
        |-----B.py

    Suppose `main.py` imports `A.py` as a module, and `A.py` in tern imports `B.py`
    as a module. Inside of `A.py`, it should use `B = repyre('./sublib/B')`,
    NOT `B = repyre('sublib/B')` since the latter will fail when `main.py`
    imports `A.py` (because the current working directory will be `top_folder`
    NOT `lib`). However, `main.py` is free to import `A.py` as `A = repyre('lib/A')`
    or `A = repyre('./lib/A')` provided `main.py` will only ever be run directly
    as a script from `top_folder`.

    Paramters
    ---------
    path : str
        The path and name of the module to be imported. This can either be a
        module readily findable from the current `sys.path` (like all the standard
        library and pip installs -- e.g. `repyre('os')` or `repyre('json')` --
        but also other .py files in the current working directory), or a module
        in another directory refernced relatively or absolutely.

    force_reload : bool
        This boolean indicates if the specified module should be foreably
        reloaded. This is useful in the case of of name collisions between
        different modules which both must be imported. i.e. calling `repyre('lib/module')`
        and `repyre('other_lib/module')` will only successfully import the first
        module unless this flag is set on the second import. See `sys.modules`
        for more details on forcing module reloads.

    Example Usage
    -------------

    >>> os = repyre('os') # import standard library
    >>> np = repyre('numpy') # import other libraries installed with pip, etc.
    >>> plt = repyre('matplotlib.pyplot') # import sub-modules using '.' notation
    >>> A = repyre('my_dev_lib/module_A') # import modules from a relative directory path (relative to CWD)
    >>> B = repyre('../my_other_lib/module_B') # can use '..' in directory paths
    >>> adjacent = repyre('./adjacent_file') # import other files relative to this file

    """
    local_file, _path = re.match("([.][/])?(.*)",path).groups()
    _path, module_name = os.path.split(_path)
    if not local_file is None:
        _path = os.path.join(sys.path[0],_path)
    if force_reload:
        try:
            del sys.modules[module_name]
        except KeyError:
            pass

    sys.path.insert(0,_path)
    try:
        return import_module(module_name)
    finally:
        sys.path.pop(0)
