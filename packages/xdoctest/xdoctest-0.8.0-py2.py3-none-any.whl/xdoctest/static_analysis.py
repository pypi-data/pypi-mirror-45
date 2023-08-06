# -*- coding: utf-8 -*-
"""
The core logic that allows for xdoctest to parse source statically
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys
import ast
import re
import six
import tokenize
from collections import deque, OrderedDict
from os.path import (join, exists, expanduser, abspath, split, splitext,
                     isfile, dirname, basename, isdir, realpath, relpath)
from xdoctest import utils


class CallDefNode(object):
    """
    Attributes:
        doclineno (int): the line number (1 based) the docstring begins on
        doclineno_end (int): the line number (1 based) the docstring ends on
    """
    def __init__(self, callname, lineno, docstr, doclineno, doclineno_end,
                 args=None):
        self.callname = callname
        self.lineno = lineno
        self.docstr = docstr
        self.doclineno = doclineno
        self.doclineno_end = doclineno_end
        self.lineno_end = None
        self.args = args

    # def __str__(self):
    #     return '{}[{}:{}][{}]'.format(
    #         self.callname, self.lineno, self.lineno_end,
    #         self.doclineno)


class TopLevelVisitor(ast.NodeVisitor):
    """
    Parses top-level function names and docstrings

    References:
        # For other visit_<classname> values see
        http://greentreesnakes.readthedocs.io/en/latest/nodes.html

    CommandLine:
        python -m xdoctest.static_analysis TopLevelVisitor

    Example:
        >>> from xdoctest.static_analysis import *  # NOQA
        >>> from xdoctest import utils
        >>> source = utils.codeblock(
        ...    '''
        ...    def foo():
        ...        \"\"\" my docstring \"\"\"
        ...        def subfunc():
        ...            pass
        ...    def bar():
        ...        pass
        ...    class Spam(object):
        ...        def eggs(self):
        ...            pass
        ...        @staticmethod
        ...        def hams():
        ...            pass
        ...    ''')
        >>> self = TopLevelVisitor.parse(source)
        >>> callnames = set(self.calldefs.keys())
        >>> assert callnames == {'foo', 'bar', 'Spam', 'Spam.eggs', 'Spam.hams'}
        >>> assert self.calldefs['foo'].docstr.strip() == 'my docstring'
        >>> assert 'subfunc' not in self.calldefs
    """
    @classmethod
    def parse(cls, source):
        """
        main entry point

        executes parsing algorithm and populates self.calldefs
        """
        self = cls(source)
        pt = self.syntax_tree()

        self.visit(pt)

        lineno_end = source.count('\n') + 2  # one indexing
        self.process_finished(lineno_end)
        return self

    def __init__(self, source=None):
        super(TopLevelVisitor, self).__init__()
        self.calldefs = OrderedDict()
        self.source = source
        self.sourcelines = None

        self._current_classname = None
        # Keep track of when we leave a top level definition
        self._finish_queue = deque()

        # new
        self.assignments = []

    def syntax_tree(self):
        """ creates the abstract syntax tree """
        self.sourcelines = self.source.splitlines()
        source_utf8  = self.source.encode('utf8')
        pt = ast.parse(source_utf8)
        return pt

    def process_finished(self, node):
        """ process (get ending lineno) for everything marked as finished """
        if self._finish_queue:
            if isinstance(node, int):
                lineno_end = node
            else:
                lineno_end = getattr(node, 'lineno', None)
            while self._finish_queue:
                calldef = self._finish_queue.pop()
                calldef.lineno_end = lineno_end

    def visit(self, node):
        self.process_finished(node)
        super(TopLevelVisitor, self).visit(node)

    def visit_FunctionDef(self, node):
        if self._current_classname is None:
            callname = node.name
        else:
            callname = self._current_classname + '.' + node.name

        lineno = self._workaround_func_lineno(node)
        docstr, doclineno, doclineno_end = self._get_docstring(node)
        calldef = CallDefNode(callname, lineno, docstr, doclineno,
                              doclineno_end, args=node.args)
        self.calldefs[callname] = calldef

        self._finish_queue.append(calldef)

    def visit_ClassDef(self, node):
        if self._current_classname is None:
            callname = node.name
            self._current_classname = callname
            docstr, doclineno, doclineno_end = self._get_docstring(node)
            calldef = CallDefNode(callname, node.lineno, docstr, doclineno,
                                  doclineno_end)
            self.calldefs[callname] = calldef

            self.generic_visit(node)
            self._current_classname = None

            self._finish_queue.append(calldef)

    def visit_Module(self, node):
        # get the module level docstr
        docstr, doclineno, doclineno_end = self._get_docstring(node)
        if docstr:
            # the module level docstr is not really a calldef, but parse it for
            # backwards compatibility.
            callname = '__doc__'
            calldef = CallDefNode(callname, doclineno, docstr, doclineno,
                                  doclineno_end)
            self.calldefs[callname] = calldef

        self.generic_visit(node)
        # self._finish_queue.append(calldef)

    def visit_Assign(self, node):
        # print('VISIT FunctionDef node = %r' % (node,))
        # print('VISIT FunctionDef node = %r' % (node.__dict__,))
        if self._current_classname is None:
            for target in node.targets:
                if hasattr(target, 'id'):
                    self.assignments.append(target.id)
            # print('node.value = %r' % (node.value,))
            # TODO: assign constants to
            # self.const_lookup
        self.generic_visit(node)

    def visit_If(self, node):
        if isinstance(node.test, ast.Compare):  # pragma: nobranch
            try:
                if all([
                    isinstance(node.test.ops[0], ast.Eq),
                    node.test.left.id == '__name__',
                    node.test.comparators[0].s == '__main__',
                ]):
                    # Ignore main block
                    return
            except Exception:  # nocover
                pass
        self.generic_visit(node)  # nocover

    # def visit_ExceptHandler(self, node):
    #     pass

    # def visit_TryFinally(self, node):
    #     pass

    # def visit_TryExcept(self, node):
    #     pass

    # def visit_Try(self, node):
    #     TODO: parse a node only if it is visible in all cases
    #     pass
    #     # self.generic_visit(node)  # nocover

    # -- helpers ---

    def _docnode_line_workaround(self, docnode):
        # lineno points to the last line of a string
        endpos = docnode.lineno - 1
        docstr = utils.ensure_unicode(docnode.value.s)
        sourcelines = self.sourcelines
        start, stop = self._docstr_line_workaround(docstr, sourcelines, endpos)
        # Convert 0-based line positions to 1-based line numbers
        doclineno = start + 1
        doclineno_end = stop
        # print('docnode = {!r}'.format(docnode))
        return doclineno, doclineno_end

    def _docstr_line_workaround(self, docstr, sourcelines, endpos):
        r"""
        Args:
            docstr (str): the extracted docstring.

            sourcelines (list): a list of all lines in the file. We assume
                the docstring exists as a pure string literal in the source.
                In other words, no postprocessing via split, format, or any
                other dynamic programatic modification should be made to the
                docstrings. Python's docstring extractor assumes this as well.

            endpos (int): line position (starting at 0) the docstring ends on.
                Note: positions are 0 based but linenos are 1 based.

        Returns:
            tuple[Int, Int]: start, stop:
                start: the line position (0 based) the docstring starts on
                stop: the line position (0 based) that the docstring stops

                such that sourcelines[start:stop] will contain the docstring
        CommandLine:
            python -m xdoctest.static_analysis TopLevelVisitor._docstr_line_workaround

        Example:
            >>> from xdoctest.static_analysis import *
            >>> sq = chr(39)  # single quote
            >>> dq = chr(34)  # double quote
            >>> source = utils.codeblock(
                '''
                def func0():
                    {ddd} docstr0 {ddd}
                def func1():
                    {ddd}
                    docstr1 {ddd}
                def func2():
                    {ddd} docstr2
                    {ddd}
                def func3():
                    {ddd}
                    docstr3
                    {ddd}  # foobar
                def func5():
                    {ddd}pathological case
                    {sss} # {ddd} # {sss} # {ddd} # {ddd}
                def func6():
                    " single quoted docstr "
                def func7():
                    r{ddd}
                    raw line
                    {ddd}
                ''').format(ddd=dq * 3, sss=sq * 3)
            >>> print(utils.add_line_numbers(utils.highlight_code(source), start=0))
            >>> targets = [
            >>>     (1, 2),
            >>>     (3, 5),
            >>>     (6, 8),
            >>>     (9, 12),
            >>>     (13, 15),
            >>>     (16, 17),
            >>>     (18, 21),
            >>> ]
            >>> self = TopLevelVisitor.parse(source)
            >>> pt = ast.parse(source.encode('utf8'))
            >>> print('\n\n====\n\n')
            >>> for i in range(len(targets)):
            >>>     print('----------')
            >>>     sourcelines = source.splitlines()
            >>>     funcnode = pt.body[i]
            >>>     docnode = funcnode.body[0]
            >>>     docstr = ast.get_docstring(funcnode, clean=False)
            >>>     endpos = docnode.lineno - 1
            >>>     start, end = self._docstr_line_workaround(docstr, sourcelines, endpos)
            >>>     print('got  = {}, {}'.format(start, end))
            >>>     print('want = {}, {}'.format(*targets[i]))
            >>>     assert targets[i] == (start, end)
            >>>     print('----------')
        """
        # First assume a one-line string that starts and stops on the same line
        start = endpos
        stop = endpos + 1

        # Determine if the docstring is a triple quoted string, by trying both
        # triple quote styles and checking if the string starts and ends with
        # the same style. If both cases are true we know we are in a triple
        # quoted string literal and can therefore safely extract the starting
        # line position.
        trips = ("'''", '"""')
        endline = sourcelines[stop - 1]
        for trip in trips:
            pattern = re.escape(trip) + r'\s*#.*$'
            # Assuming the multiline string is using `trip` as the triple quote
            # format, then the first instance of that pattern must terminate
            # the string literal. Afterwords the only valid characters are
            # whitespace and comments. Anything after the comment can be
            # ignored. The above pattern will match the first triple quote it
            # sees, and then will remove any trailing comments.
            endline_ = re.sub(pattern, trip, endline).strip()
            # After removing commends, if the endline endswith a triple quote,
            # then we must be in a multiline string IF the startline starts
            # with that same triple quote. We should be able to determine where
            # the startline is because we know how many newline characters are
            # in the extracted docstring. This works because all newline
            # characters in multiline string literals MUST correspond to actual
            # newlines in the source code.
            if endline_.endswith(trip):
                nlines = docstr.count('\n')
                # assuming that the docstr is actually terminated with this
                # kind of triple quote, then the start line is at this position
                cand_start_ = stop - nlines - 1
                startline = sourcelines[cand_start_]

                # The startline should also begin with the same triple quote
                # Account for raw strings. Note f-strings cannot be docstrings
                if startline.strip().startswith((trip, 'r' + trip)):
                    # Both conditions pass.
                    start = cand_start_
                    break
                else:
                    # Conditions failed, revert to assuming a one-line string.
                    start = stop - 1

        return start, stop

    def _get_docstring(self, node):
        """
        Example:
            >>> source = utils.codeblock(
                '''
                def foo():
                    'docstr'
                ''')
            >>> self = TopLevelVisitor(source)
            >>> node = self.syntax_tree().body[0]
            >>> self._get_docstring(node)
            ('docstr', 2, 2)
        """
        docstr = ast.get_docstring(node, clean=False)
        if docstr is not None:
            docnode = node.body[0]
            doclineno, doclineno_end = self._docnode_line_workaround(docnode)
        else:
            doclineno = None
            doclineno_end = None
        return (docstr, doclineno, doclineno_end)

    def _workaround_func_lineno(self, node):
        """
        Example:
            >>> source = utils.codeblock(
                '''
                @bar
                @baz
                def foo():
                    'docstr'
                ''')
            >>> self = TopLevelVisitor(source)
            >>> node = self.syntax_tree().body[0]
            >>> self._workaround_func_lineno(node)
            3
        """
        # Try and find the lineno of the function definition
        # (maybe the fact that its on a decorator is actually right...)
        if node.decorator_list:
            # Decorators can throw off the line the function is declared on
            linex = node.lineno - 1
            pattern = r'\s*def\s*' + node.name
            # I think this is actually robust
            while not re.match(pattern, self.sourcelines[linex]):
                linex += 1
            lineno = linex + 1
        else:
            lineno = node.lineno
        return lineno


def parse_calldefs(source=None, fpath=None):
    """
    Statically finds top-level callable functions and methods in python source

    Args:
        source (str): python text
        fpath (str): filepath to read if source is not specified

    Returns:
        dict(str, CallDefNode): map of callnames to tuples with def info

    Example:
        >>> from xdoctest import static_analysis
        >>> fpath = static_analysis.__file__.replace('.pyc', '.py')
        >>> calldefs = parse_calldefs(fpath=fpath)
        >>> assert 'parse_calldefs' in calldefs
    """
    if six.PY2:
        fpath = fpath.replace('.pyc', '.py')

    if source is None:  # pragma: no branch
        try:
            with open(fpath, 'rb') as file_:
                source = file_.read().decode('utf-8')
        except Exception as ex:
            try:
                with open(fpath, 'rb') as file_:
                    source = file_.read()
            except Exception:
                print('Unable to read fpath = {!r}'.format(fpath))
                raise
    try:
        self = TopLevelVisitor.parse(source)
        return self.calldefs
    except Exception:  # nocover
        if fpath:
            print('Failed to parse docstring for fpath=%r' % (fpath,))
        else:
            print('Failed to parse docstring')
        raise


def _parse_static_node_value(node):
    """
    Extract a constant value from a node if possible
    """
    if isinstance(node, ast.Num):
        value = node.n
    elif isinstance(node, ast.Str):
        value = node.s
    elif isinstance(node, ast.List):
        value = list(map(_parse_static_node_value, node.elts))
    elif isinstance(node, ast.Tuple):
        value = tuple(map(_parse_static_node_value, node.elts))
    elif isinstance(node, (ast.Dict)):
        keys = map(_parse_static_node_value, node.keys)
        values = map(_parse_static_node_value, node.values)
        value = OrderedDict(zip(keys, values))
        # value = dict(zip(keys, values))
    elif six.PY3 and isinstance(node, (ast.NameConstant)):
        value = node.value
    elif (six.PY2 and isinstance(node, ast.Name) and
          node.id in ['None', 'True', 'False']):
        # disregard pathological python2 corner cases
        value = {'None': None, 'True': True, 'False': False}[node.id]
    else:
        print(node.__dict__)
        raise TypeError('Cannot parse a static value from non-static node '
                        'of type: {!r}'.format(type(node)))
    return value


def parse_static_value(key, source=None, fpath=None):
    """
    Statically parse a constant variable's value from python code.

    TODO: This does not belong here. Move this to an external static analysis
    library.

    Args:
        key (str): name of the variable
        source (str): python text
        fpath (str): filepath to read if source is not specified

    Example:
        >>> from xdoctest.static_analysis import parse_static_value
        >>> key = 'foo'
        >>> source = 'foo = 123'
        >>> assert parse_static_value(key, source=source) == 123
        >>> source = 'foo = "123"'
        >>> assert parse_static_value(key, source=source) == '123'
        >>> source = 'foo = [1, 2, 3]'
        >>> assert parse_static_value(key, source=source) == [1, 2, 3]
        >>> source = 'foo = (1, 2, "3")'
        >>> assert parse_static_value(key, source=source) == (1, 2, "3")
        >>> source = 'foo = {1: 2, 3: 4}'
        >>> assert parse_static_value(key, source=source) == {1: 2, 3: 4}
        >>> source = 'foo = None'
        >>> assert parse_static_value(key, source=source) == None
        >>> #parse_static_value('bar', source=source)
        >>> #parse_static_value('bar', source='foo=1; bar = [1, foo]')
    """
    if source is None:  # pragma: no branch
        try:
            with open(fpath, 'rb') as file_:
                source = file_.read().decode('utf-8')
        except Exception as ex:
            with open(fpath, 'rb') as file_:
                source = file_.read()
    pt = ast.parse(source)

    class AssignentVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            for target in node.targets:
                target_id = getattr(target, 'id', None)
                if target_id == key:
                    self.value = _parse_static_node_value(node.value)

    sentinal = object()
    visitor = AssignentVisitor()
    visitor.value = sentinal
    visitor.visit(pt)
    if visitor.value is sentinal:
        raise NameError('No static variable named {!r}'.format(key))
    return visitor.value


def _extension_module_tags():
    """
    Returns valid tags an extension module might have
    """
    import sysconfig
    tags = []
    if six.PY2:
        # see also 'SHLIB_EXT'
        multiarch = sysconfig.get_config_var('MULTIARCH')
        if multiarch is not None:
            tags.append(multiarch)
    else:
        # handle PEP 3149 -- ABI version tagged .so files
        # ABI = application binary interface
        tags.append(sysconfig.get_config_var('SOABI'))
        tags.append('abi3')  # not sure why this one is valid but it is
    tags = [t for t in tags if t]
    return tags


def _platform_pylib_exts():  # nocover
    """
    Returns .so, .pyd, or .dylib depending on linux, win or mac.
    On python3 return the previous with and without abi (e.g.
    .cpython-35m-x86_64-linux-gnu) flags. On python2 returns with
    and without multiarch.
    """
    import sysconfig
    valid_exts = []
    if six.PY2:
        # see also 'SHLIB_EXT'
        base_ext = '.' + sysconfig.get_config_var('SO').split('.')[-1]
    else:
        # return with and without API flags
        # handle PEP 3149 -- ABI version tagged .so files
        base_ext = '.' + sysconfig.get_config_var('EXT_SUFFIX').split('.')[-1]
    for tag in _extension_module_tags():
        valid_exts.append('.' + tag + base_ext)
    valid_exts.append(base_ext)
    return tuple(valid_exts)


def normalize_modpath(modpath, hide_init=True, hide_main=False):
    """
    Normalizes __init__ and __main__ paths.

    Notes:
        Adds __init__ if reasonable, but only removes __main__ by default

    Args:
        hide_init (bool): if True, always return package modules
           as __init__.py files otherwise always return the dpath.
        hide_init (bool): if True, always strip away main files otherwise
           ignore __main__.py.

    CommandLine:
        xdoctest -m xdoctest.static_analysis normalize_modpath

    Example:
        >>> import xdoctest.static_analysis as static
        >>> modpath = static.__file__
        >>> assert static.normalize_modpath(modpath) == modpath.replace('.pyc', '.py')
        >>> dpath = dirname(modpath)
        >>> res0 = static.normalize_modpath(dpath, hide_init=0, hide_main=0)
        >>> res1 = static.normalize_modpath(dpath, hide_init=0, hide_main=1)
        >>> res2 = static.normalize_modpath(dpath, hide_init=1, hide_main=0)
        >>> res3 = static.normalize_modpath(dpath, hide_init=1, hide_main=1)
        >>> assert res0.endswith('__init__.py')
        >>> assert res1.endswith('__init__.py')
        >>> assert not res2.endswith('.py')
        >>> assert not res3.endswith('.py')
    """
    if six.PY2:
        if modpath.endswith('.pyc'):
            modpath = modpath[:-1]
    if hide_init:
        if basename(modpath) == '__init__.py':
            modpath = dirname(modpath)
            hide_main = True
    else:
        # add in init, if reasonable
        modpath_with_init = join(modpath, '__init__.py')
        if exists(modpath_with_init):
            modpath = modpath_with_init
    if hide_main:
        # We can remove main, but dont add it
        if basename(modpath) == '__main__.py':
            # corner case where main might just be a module name not in a pkg
            parallel_init = join(dirname(modpath), '__init__.py')
            if exists(parallel_init):
                modpath = dirname(modpath)
    return modpath


def package_modpaths(pkgpath, with_pkg=False, with_mod=True, followlinks=True,
                     recursive=True, with_libs=False, check=True):
    r"""
    Finds sub-packages and sub-modules belonging to a package.

    Args:
        pkgpath (str): path to a module or package
        with_pkg (bool): if True includes package __init__ files (default =
            False)
        with_mod (bool): if True includes module files (default = True)
        exclude (list): ignores any module that matches any of these patterns
        recursive (bool): if False, then only child modules are included
        with_libs (bool): if True then compiled shared libs will be returned as well
        check (bool): if False, then then pkgpath is considered a module even
            if it does not contain an __init__ file.

    Yields:
        str: module names belonging to the package

    References:
        http://stackoverflow.com/questions/1707709/list-modules-in-py-package

    Example:
        >>> from xdoctest.static_analysis import *
        >>> pkgpath = modname_to_modpath('xdoctest')
        >>> paths = list(package_modpaths(pkgpath))
        >>> print('\n'.join(paths))
        >>> names = list(map(modpath_to_modname, paths))
        >>> assert 'xdoctest.core' in names
        >>> assert 'xdoctest.__main__' in names
        >>> assert 'xdoctest' not in names
        >>> print('\n'.join(names))
    """
    if isfile(pkgpath):
        # If input is a file, just return it
        yield pkgpath
    else:
        if with_pkg:
            root_path = join(pkgpath, '__init__.py')
            if not check or exists(root_path):
                yield root_path

        valid_exts = ['.py']
        if with_libs:
            valid_exts += _platform_pylib_exts()

        for dpath, dnames, fnames in os.walk(pkgpath, followlinks=followlinks):
            ispkg = exists(join(dpath, '__init__.py'))
            if ispkg or not check:
                check = True  # always check subdirs
                if with_mod:
                    for fname in fnames:
                        if splitext(fname)[1] in valid_exts:
                            # dont yield inits. Handled in pkg loop.
                            if fname != '__init__.py':
                                path = join(dpath, fname)
                                yield path
                if with_pkg:
                    for dname in dnames:
                        path = join(dpath, dname, '__init__.py')
                        if exists(path):
                            yield path
            else:
                # Stop recursing when we are out of the package
                del dnames[:]
            if not recursive:
                break


def split_modpath(modpath, check=True):
    """
    Splits the modpath into the dir that must be in PYTHONPATH for the module
    to be imported and the modulepath relative to this directory.

    Args:
        modpath (str): module filepath
        check (bool): if False, does not raise an error if modpath is a
            directory and does not contain an `__init__.py` file.

    Returns:
        tuple: (directory, rel_modpath)

    Raises:
        ValueError: if modpath does not exist or is not a package

    Example:
        >>> from xdoctest import static_analysis
        >>> modpath = static_analysis.__file__.replace('.pyc', '.py')
        >>> modpath = abspath(modpath)
        >>> dpath, rel_modpath = split_modpath(modpath)
        >>> recon = join(dpath, rel_modpath)
        >>> assert recon == modpath
        >>> assert rel_modpath == join('xdoctest', 'static_analysis.py')
    """
    if six.PY2:
        if modpath.endswith('.pyc'):
            modpath = modpath[:-1]
    modpath_ = abspath(expanduser(modpath))
    if check:
        if not exists(modpath_):
            if not exists(modpath):
                raise ValueError('modpath={} does not exist'.format(modpath))
            raise ValueError('modpath={} is not a module'.format(modpath))
        if isdir(modpath_) and not exists(join(modpath, '__init__.py')):
            # dirs without inits are not modules
            raise ValueError('modpath={} is not a module'.format(modpath))
    full_dpath, fname_ext = split(modpath_)
    _relmod_parts = [fname_ext]
    # Recurse down directories until we are out of the package
    dpath = full_dpath
    while exists(join(dpath, '__init__.py')):
        dpath, dname = split(dpath)
        _relmod_parts.append(dname)
    relmod_parts = _relmod_parts[::-1]
    rel_modpath = os.path.sep.join(relmod_parts)
    return dpath, rel_modpath


def modpath_to_modname(modpath, hide_init=True, hide_main=False, check=True,
                       relativeto=None):
    """
    Determines importable name from file path

    Converts the path to a module (__file__) to the importable python name
    (__name__) without importing the module.

    The filename is converted to a module name, and parent directories are
    recursively included until a directory without an __init__.py file is
    encountered.

    Args:
        modpath (str): module filepath
        hide_init (bool): removes the __init__ suffix (default True)
        hide_main (bool): removes the __main__ suffix (default False)
        check (bool): if False, does not raise an error if modpath is a dir
            and does not contain an __init__ file.
        relativeto (str, optional): if specified, all checks are ignored and
            this is considered the path to the root module.

    Returns:
        str: modname

    Raises:
        ValueError: if check is True and the path does not exist

    CommandLine:
        xdoctest -m xdoctest.static_analysis modpath_to_modname

    Example:
        >>> from xdoctest import static_analysis
        >>> modpath = static_analysis.__file__.replace('.pyc', '.py')
        >>> modpath = modpath.replace('.pyc', '.py')
        >>> modname = modpath_to_modname(modpath)
        >>> assert modname == 'xdoctest.static_analysis'

    Example:
        >>> import xdoctest
        >>> assert modpath_to_modname(xdoctest.__file__.replace('.pyc', '.py')) == 'xdoctest'
        >>> assert modpath_to_modname(dirname(xdoctest.__file__.replace('.pyc', '.py'))) == 'xdoctest'

    Example:
        >>> modpath = modname_to_modpath('_ctypes')
        >>> modname = modpath_to_modname(modpath)
        >>> assert modname == '_ctypes'
    """
    if check and relativeto is None:
        if not exists(modpath):
            raise ValueError('modpath={} does not exist'.format(modpath))
    modpath_ = abspath(expanduser(modpath))

    modpath_ = normalize_modpath(modpath_, hide_init=hide_init,
                                 hide_main=hide_main)
    if relativeto:
        dpath = dirname(abspath(expanduser(relativeto)))
        rel_modpath = relpath(modpath_, dpath)
    else:
        dpath, rel_modpath = split_modpath(modpath_, check=check)

    modname = splitext(rel_modpath)[0]
    if '.' in modname:
        modname, abi_tag = modname.split('.')
    modname = modname.replace('/', '.')
    modname = modname.replace('\\', '.')
    return modname


def modname_to_modpath(modname, hide_init=True, hide_main=False, sys_path=None):
    """
    Finds the path to a python module from its name.

    Determines the path to a python module without directly import it

    Converts the name of a module (__name__) to the path (__file__) where it is
    located without importing the module. Returns None if the module does not
    exist.

    Args:
        modname (str): module filepath
        hide_init (bool): if False, __init__.py will be returned for packages
        hide_main (bool): if False, and hide_init is True, __main__.py will be
            returned for packages, if it exists.
        sys_path (list): if specified overrides `sys.path` (default None)

    Returns:
        str: modpath - path to the module, or None if it doesn't exist

    CommandLine:
        python -m xdoctest.static_analysis modname_to_modpath:0
        pytest  /home/joncrall/code/xdoctest/xdoctest/static_analysis.py::modname_to_modpath:0

    Example:
        >>> modname = 'xdoctest.__main__'
        >>> modpath = modname_to_modpath(modname, hide_main=False)
        >>> assert modpath.endswith('__main__.py')
        >>> modname = 'xdoctest'
        >>> modpath = modname_to_modpath(modname, hide_init=False)
        >>> assert modpath.endswith('__init__.py')
        >>> modpath = basename(modname_to_modpath('_ctypes'))
        >>> assert 'ctypes' in modpath
    """
    modpath = _syspath_modname_to_modpath(modname, sys_path)
    if modpath is None:
        return None

    modpath = normalize_modpath(modpath, hide_init=hide_init,
                                hide_main=hide_main)
    return modpath


def _pkgutil_modname_to_modpath(modname):  # nocover
    """
    faster version of `_syspath_modname_to_modpath` using builtin python
    mechanisms, but unfortunately it doesn't play nice with pytest.

    Example:
        >>> # xdoctest: +SKIP
        >>> modname = 'xdoctest.static_analysis'
        >>> _pkgutil_modname_to_modpath(modname)
        ...static_analysis.py
        >>> _pkgutil_modname_to_modpath('_ctypes')
        ..._ctypes...

    Ignore:
        >>> _pkgutil_modname_to_modpath('cv2')
    """
    import pkgutil
    loader = pkgutil.find_loader(modname)
    if loader is None:
        raise Exception('No module named {} in the PYTHONPATH'.format(modname))
    modpath = loader.get_filename().replace('.pyc', '.py')
    return modpath


def _syspath_modname_to_modpath(modname, sys_path=None, exclude=None):
    """
    syspath version of modname_to_modpath

    Args:
        modname (str): name of module to find
        sys_path (List[PathLike], default=None):
            if specified overrides `sys.path`
        exclude (List[PathLike], default=None):
            list of directory paths. if specified prevents these directories
            from being searched.

    Notes:
        This is much slower than the pkgutil mechanisms.

    CommandLine:
        python -m xdoctest.static_analysis _syspath_modname_to_modpath

    Example:
        >>> print(_syspath_modname_to_modpath('xdoctest.static_analysis'))
        ...static_analysis.py
        >>> print(_syspath_modname_to_modpath('xdoctest'))
        ...xdoctest
        >>> print(_syspath_modname_to_modpath('_ctypes'))
        ..._ctypes...
        >>> assert _syspath_modname_to_modpath('xdoctest', sys_path=[]) is None
        >>> assert _syspath_modname_to_modpath('xdoctest.static_analysis', sys_path=[]) is None
        >>> assert _syspath_modname_to_modpath('_ctypes', sys_path=[]) is None
        >>> assert _syspath_modname_to_modpath('this', sys_path=[]) is None

    Example:
        >>> # test what happens when the module is not visible in the path
        >>> modname = 'xdoctest.static_analysis'
        >>> modpath = _syspath_modname_to_modpath(modname)
        >>> exclude = [split_modpath(modpath)[0]]
        >>> found = _syspath_modname_to_modpath(modname, exclude=exclude)
        >>> # this only works if installed in dev mode, pypi fails
        >>> assert found is None, 'should not have found {}'.format(found)
    """

    def _isvalid(modpath, base):
        # every directory up to the module, should have an init
        subdir = dirname(modpath)
        while subdir and subdir != base:
            if not exists(join(subdir, '__init__.py')):
                return False
            subdir = dirname(subdir)
        return True

    _fname_we = modname.replace('.', os.path.sep)
    candidate_fnames = [
        _fname_we + '.py',
        # _fname_we + '.pyc',
        # _fname_we + '.pyo',
    ]
    # Add extension library suffixes
    candidate_fnames += [_fname_we + ext for ext in _platform_pylib_exts()]

    if sys_path is None:
        sys_path = sys.path

    # the empty string in sys.path indicates cwd. Change this to a '.'
    candidate_dpaths = ['.' if p == '' else p for p in sys_path]

    if exclude:
        def normalize(p):
            if sys.platform.startswith('win32'):  # nocover
                return realpath(p).lower()
            else:
                return realpath(p)
        # Keep only the paths not in exclude
        real_exclude = {normalize(p) for p in exclude}
        candidate_dpaths = [p for p in candidate_dpaths
                            if normalize(p) not in real_exclude]

    for dpath in candidate_dpaths:
        # Check for directory-based modules (has presidence over files)
        modpath = join(dpath, _fname_we)
        if exists(modpath):
            if isfile(join(modpath, '__init__.py')):
                if _isvalid(modpath, dpath):
                    return modpath

        # If that fails, check for file-based modules
        for fname in candidate_fnames:
            modpath = join(dpath, fname)
            if isfile(modpath):
                if _isvalid(modpath, dpath):
                    return modpath


def is_modname_importable(modname, sys_path=None, exclude=None):
    """
    Determines if a modname is importable based on your current sys.path

    Args:
        modname (str): name of module to check
        sys_path (list): if specified overrides `sys.path` (default None)
        exclude (list): list of directory paths. if specified prevents these
            directories from being searched.

    Returns:
        bool: True if the module could be imported

    Example:
        >>> is_modname_importable('xdoctest')
        True
        >>> is_modname_importable('not_a_real_module')
        False
        >>> is_modname_importable('xdoctest', sys_path=[])
        False
    """
    modpath = _syspath_modname_to_modpath(modname, sys_path=sys_path,
                                          exclude=exclude)
    flag = bool(modpath is not None)
    return flag


def is_balanced_statement(lines, only_tokens=False):
    r"""
    Checks if the lines have balanced parens, brakets, curlies and strings

    Args:
        lines (list): list of strings

    Returns:
        bool: False if the statement is not balanced

    CommandLine:
        xdoctest -m xdoctest.static_analysis is_balanced_statement

    Doctest:
        >>> assert is_balanced_statement(['print(foobar)'])
        >>> assert is_balanced_statement(['foo = bar']) is True
        >>> assert is_balanced_statement(['foo = (']) is False
        >>> assert is_balanced_statement(['foo = (', "')(')"]) is True
        >>> assert is_balanced_statement(
        ...     ['foo = (', "'''", ")]'''", ')']) is True
        >>> assert is_balanced_statement(
        ...     ['foo = ', "'''", ")]'''", ')']) is False
        >>> #assert is_balanced_statement(['foo = ']) is False
        >>> #assert is_balanced_statement(['== ']) is False
        >>> lines = ['def foo():', '', '    x = 1', 'assert True', '']
        >>> assert is_balanced_statement(lines)

    Doctest:
        >>> from xdoctest.static_analysis import *
        >>> source_parts = [
        >>>     'setup(',
        >>>     "    name='extension',",
        >>>     '    ext_modules=[',
        >>>     '        CppExtension(',
        >>>     "            name='extension',",
        >>>     "            sources=['extension.cpp'],",
        >>>     "            extra_compile_args=['-g'])),",
        >>>     '    ],',
        >>> ]
        >>> print('\n'.join(source_parts))
        >>> assert not is_balanced_statement(source_parts)
        >>> source_parts = [
        >>>     'setup(',
        >>>     "    name='extension',",
        >>>     '    ext_modules=[',
        >>>     '        CppExtension(',
        >>>     "            name='extension',",
        >>>     "            sources=['extension.cpp'],",
        >>>     "            extra_compile_args=['-g']),",
        >>>     '    ],',
        >>>     '        cmdclass={',
        >>>     "            'build_ext': BuildExtension",
        >>>     '        })',
        >>> ]
        >>> print('\n'.join(source_parts))
        >>> assert is_balanced_statement(source_parts)
    """
    # Only iterate through non-empty lines otherwise tokenize will stop short
    lines = list(lines)
    iterable = (line for line in lines if line)
    def _readline():
        return next(iterable)
    try:
        for t in tokenize.generate_tokens(_readline):
            pass
    except tokenize.TokenError as ex:
        message = ex.args[0]
        if message.startswith('EOF in multi-line'):
            return False
        raise
    except IndentationError as ex:
        message = ex.args[0]
        if message.startswith('unindent does not match any outer indentation'):
            return False
        raise
    else:
        # Note: trying to use ast.parse(block) will not work
        # here because it breaks in try, except, else
        if not only_tokens:
            # The above test wont trigger for cases involving higher level
            # python grammar. If we wish to test for these we will have to use
            # an AST.
            try:
                text = '\n'.join(lines)
                # from textwrap import dedent
                # text = dedent(text)
                six_axt_parse(text)
            except SyntaxError:
                return False

        return True


def extract_comments(source):
    """
    Returns the text in each comment in a block of python code.
    Uses tokenize to account for quotations.

    CommandLine:
        python -m xdoctest.static_analysis extract_comments

    Example:
        >>> from xdoctest import utils
        >>> source = utils.codeblock(
        >>>    '''
               # comment 1
               a = '# not a comment'  # comment 2
               c = 3
               ''')
        >>> comments = list(extract_comments(source))
        >>> assert comments == ['# comment 1', '# comment 2']
        >>> comments = list(extract_comments(source.splitlines()))
        >>> assert comments == ['# comment 1', '# comment 2']
    """
    if isinstance(source, six.string_types):
        lines = source.splitlines()
    else:
        lines = source

    # Only iterate through non-empty lines otherwise tokenize will stop short
    iterable = (line for line in lines if line)
    def _readline():
        return next(iterable)
    try:
        for t in tokenize.generate_tokens(_readline):
            if t[0] == tokenize.COMMENT:
                yield t[1]
    except tokenize.TokenError as ex:
        pass


def six_axt_parse(source_block, filename='<source_block>', compatible=True):
    """
    Python 2/3 compatible replacement for ast.parse(source_block, filename='<source_block>')
    """
    # Note Python2.7 does not accept unicode variable names so this
    # will fail (in 2.7) if source contains a unicode varname.
    if compatible and six.PY2:
        # In Python2.7 fix __future__ issues
        import __future__
        flags = ast.PyCF_ONLY_AST
        flags |= __future__.print_function.compiler_flag
        # flags |= __future__.print_function.unicode_literals
        pt = compile(source_block, filename=filename, mode='exec', flags=flags)
    else:
        pt = ast.parse(source_block, filename=filename)
    return pt


if __name__ == '__main__':
    import xdoctest as xdoc
    xdoc.doctest_module()
