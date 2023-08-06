# -*- coding: utf-8 -*-
"""
File utilities for spines.
"""
#
#   Imports
#
import os
import pickle
import tarfile
from typing import List
from typing import Tuple
import zipfile


#
#   Constants
#

_DEFAULT_ARCHIVE_FORMAT = 'zip'
_DEFAULT_TAR_COMPRESSION = 'gzip'


#
#   Functions
#

def save_pickle(obj, *path: Tuple[str]) -> str:
    """Save a single object, pickled, to file

    Parameters
    ----------
    file : str
        Name to save the file with.
    obj
        Object to save in pickled format.

    Returns
    -------
    str
        The path of the file created.

    """
    file = os.path.join(*path)
    if not file.endswith('.pkl'):
        file += '.pkl'
    with open(file, 'wb') as fout:
        pickle.dump(obj, fout)
    return file


def load_pickle(*path: Tuple[str]) -> object:
    """Load a single pickled object from file

    Parameters
    ----------
    file : str
        File to load.

    Returns
    -------
    object
        Object loaded from file.

    """
    file = os.path.join(*path)
    if not file.endswith('.pkl'):
        file += '.pkl'
    with open(file, 'rb') as fin:
        ret = pickle.load(fin)
    return ret


def get_archive_extension(fmt: str) -> str:
    """Gets the file extension based on format given

    Parameters
    ----------
    fmt : str
        Format to get file extension for.

    Returns
    -------
    str
        File extension to use for the given format.

    """
    fmt = _clean_archive_file_format(fmt)
    if fmt == 'lzma' or fmt.startswith('xz'):
        return '.tar.xz'
    elif fmt == 'bzip2' or fmt.startswith('bz'):
        return '.tar.bz2'
    elif fmt == 'gzip' or fmt.startswith('gz'):
        return '.tar.gz'
    return '.%s' % fmt


def save_archive(
    path: str, files: List[str], fmt: [str, None] = None
) -> str:
    """Saves a set of files into a single archive file

    Parameters
    ----------
    path : str
        Path to save the archive file to.
    files : :obj:`list` of :obj:`str`
        Files to bundle into the archive.
    fmt : str, optional
        Archive file format to use.

    Returns
    -------
    str
        Path to the output archive file created.

    """
    if fmt is None:
        fmt = _DEFAULT_ARCHIVE_FORMAT
    fmt = _clean_archive_file_format(fmt)

    file_ext = get_archive_extension(fmt)
    if not path.endswith(file_ext):
        path = os.path.join(path, file_ext)

    if fmt == 'zip':
        return _save_zip_archive(path, files)
    return _save_tar_archive(path, files, fmt=fmt)


def _save_zip_archive(path: str, files: List[str]) -> str:
    """Saves the given `files` as a zip archive at the given `path`"""
    with _get_zip_archive(path, 'w') as archive:
        for file in files:
            archive.write(file, os.path.basename(file))
    return path


def _save_tar_archive(
    path: str, files: List[str], fmt: str = None
) -> str:
    """Saves the given `files` as a tar archive at the given `path`"""
    with _get_tar_archive(path, 'w', fmt=fmt) as archive:
        for file in files:
            archive.add(file, arcname=os.path.basename(file))
    return path


def extract_archive(
    path: str, output: str, fmt: [str, None] = None
) -> None:
    """Extracts the specified archive contents from file

    Parameters
    ----------
    path : str
        Archive file path to extract files from.
    output : str
        Output directory to save contents to.
    fmt : str, optional
        File format to load archive as (default is :obj:`None`, which
        will attempt to infer the format from the `path`).

    """
    if not fmt:
        fmt = _infer_archive_format(path)
    else:
        fmt = _clean_archive_file_format(fmt)

    if fmt == 'zip':
        h_archive = _get_zip_archive(path, 'r')
    else:
        h_archive = _get_tar_archive(path, 'r', fmt=fmt)

    with h_archive as archive:
        archive.extractall(output)

    return


def _get_zip_archive(path: str, mode: str):
    """Extracts the given zip file to the given output directory"""
    return zipfile.ZipFile(path, mode)


def _get_tar_archive(path: str, mode: str, fmt: [str, None] = None):
    """Get the tarfile object to extract from"""
    mode = _tar_mode_helper(mode, fmt)
    return tarfile.open(path, mode)


def _tar_mode_helper(mode: str, compression: str) -> str:
    """Get tar file mode string"""
    ret = mode
    if compression is None:
        return ret
    else:
        compression = _clean_archive_file_format(compression)

    if compression == 'lzma' or compression.startswith('xz'):
        return ret + ':xz'
    elif compression == 'gzip' or compression.startswith('gz'):
        return ret + ':gz'
    elif compression == 'bzip2' or compression.startswith('bz'):
        return ret + ':bz2'
    return ret


def _infer_archive_format(path: str) -> str:
    """Attempts to infer the archive file format from the path"""
    exts = list()
    tmp_path, tmp_ext = os.path.splitext(path)
    while tmp_ext:
        exts.append(tmp_ext)
        tmp_path, tmp_ext = os.path.splitext(tmp_path)
    exts = tuple(reversed(exts))

    if exts[0] == '.tar':
        if len(exts) == 2:
            compression = exts[1]
            if compression == '.xz':
                return 'lzma'
            elif compression == '.gz':
                return 'gzip'
            elif compression == '.bz2':
                return 'bzip2'
            else:
                return compression.strip('.').lower()
        else:
            return 'tar'
    elif exts[0] == '.zip':
        return 'zip'

    raise ValueError("Cannot infer file format, please specify")


def _clean_archive_file_format(fmt: str) -> str:
    """Cleans the given file format string"""
    return fmt.lower().strip('.').strip(':')
