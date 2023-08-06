# -*- coding: utf-8 -*-
"""
Utility functions for the spines versioning sub-package.
"""
#
#   Imports
#
import difflib
import inspect
import re
from textwrap import dedent
from types import FunctionType
from typing import Dict
from typing import List
import unicodedata

from ..vendor import autopep8 as _v_autopep8


#
#   Functions
#

def slugify(value: str, allow_unicode: bool = False) -> str:
    """Slugifys the given string

    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.

    .. note::
        Modified (barely) from Django:
        https://github.com/django/django/blob/master/django/utils/text.py

    Parameters
    ----------
    value : str
        String to slugify.
    allow_unicode : bool, optional
        Whether or not to allow unicode characters.

    Returns
    -------
    str
        Slugified string.

    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')\
                           .decode('ascii')
    value = re.sub(r'[^\w\s-]', '_', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def get_function_source(func):
    """Gets the source code for the given function

    Parameters
    ----------
    func : callable
        Function to get source code of.

    Returns
    -------
    str
        Function source code, properly formatted.

    """
    raw_source = dedent(inspect.getsource(func))
    return _v_autopep8.fix_code(raw_source)


def get_doc_string(obj):
    """Gets the documentation string for the given object

    Parameters
    ----------
    obj : object
        Object to get docstring for.

    Returns
    -------
    str
        Docstring of the given object.

    """
    return inspect.cleandoc(inspect.getdoc(obj))


def get_diff(a: [str, List[str]], b: [str, List[str]], n=3):
    """Gets the differences between text data

    Parameters
    ----------
    a : :obj:`str` or :obj:`list` of :obj:`str`
        Text to compare from.
    b : :obj:`str` or :obj:`list` of :obj:`str`
        Text to compare with.
    n : int, optional
        Lines of context to show around differences.

    Returns
    -------
    str
        Differences between the texts.

    """
    if not isinstance(a, list):
        a = a.splitlines()
    if not isinstance(b, list):
        b = b.splitlines()
    return ''.join(
        difflib.context_diff(a, b, fromfile='Current', tofile='New', n=n)
    )


def get_changes(a: [str, List[str]], b: [str, List[str]]) -> List[tuple]:
    """Gets the full set of changes required to go from a to b

    Parameters
    ----------
    a : :obj:`str` or :obj:`list` of :obj:`str`
        Text to start from.
    b : :obj:`str` or :obj:`list` of :obj:`str`
        Text to get changes to get to.

    Returns
    -------
    :obj:`list` of :obj:`tuple`
        List of five-tuples of operation, from start index, from end
        index, to start index and to end index.

    """
    if not isinstance(a, str):
        a = '\n'.join(a)
    if not isinstance(b, list):
        b = '\n'.join(b)
    s = difflib.SequenceMatcher(None, a, b)
    return s.get_opcodes()


def get_function_bytes(func: FunctionType):
    """Gets a byte-representation of a function object

    Parameters
    ----------
    func : callable
        Function to get bytes for.

    Returns
    -------
    bytes
        Byte representation of the function.
    """
    bytecode = func.__code__.co_code
    consts = func.__code__.co_consts[1:]
    dep_objs = func.__code__.co_names
    all_vars = func.__code__.co_varnames

    ret = []
    for v in (consts, dep_objs, all_vars):
        for i_v in v:
            ret.append('str:%s' % i_v)
    return bytecode + ','.join(ret).encode()


def get_function_parameters(cls, obj: FunctionType) -> Dict[str, object]:
    """Gets the parameters for a function object

    Parameters
    ----------
    func : callable
        Function to get parameters for.

    Returns
    -------
    :obj:`dict` of :obj:`str`, :obj:`object`
        Dictionary of parameter name to default value (if any, otherwise
        :obj:`None`).

    """
    fn_sig = inspect.signature(obj)
    return {
        k: None if v.default is fn_sig.empty else v.default
        for k, v in fn_sig.parameters.items()
    }
