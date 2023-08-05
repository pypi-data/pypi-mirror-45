"""
Parser that reads history files

Files can be generated by adding ``set his 1`` to the input file

"""

from numpy import empty, asfortranarray, array
from six import iteritems
from serpentTools.utils import convertVariableName, deconvertVariableName
from serpentTools.parsers.base import BaseReader
from serpentTools.messages import warning, error

__all__ = ['HistoryReader']


class ScratchStorage(object):
    """Storage container for storing arrays of potentially unknown size"""

    def __init__(self):
        self.__internals = []

    def __setitem__(self, key, value):
        if isinstance(self.__internals, list):
            self.__internals.append(value)
            return
        self.__internals[key] = value

    def __getitem__(self, key):
        return self.__internals.__getitem__(key)

    def __len__(self):
        return len(self.__internals)

    def allocate(self, shape=None, **kwargs):
        """Allocate as an empty array or list."""
        if shape is None:
            self.__internals = []
            return
        self.__internals = empty(shape, **kwargs)

    def __repr__(self):
        return self.__internals.__repr__()

    def __str__(self):
        return self.__internals.__str__()

    def __contains__(self, key):
        return self.__internals.__contains__(key)

    @property
    def data(self):
        """Return the data stored in this container."""
        if isinstance(self.__internals, list):
            return array(self.__internals)
        return self.__internals


class HistoryReader(BaseReader):
    """
    Class responsible for reading history files

    Arrays can be accessed through either the ``arrays``
    dictionary, or with ``his[key]``, where ``key`` is the
    name of an array in ``arrays``.

    Parameters
    ----------
    filePath: str
        path pointing towards the file to be read

    Attributes
    ----------
    arrays: dict
        Dictionary of all the arrays produced in the file.
        These arrays do not have the index column that is presented
        in the file.
    numInactive: int
        Number of inactive cycles used in this calculation

    """
    def __init__(self, filePath):
        BaseReader.__init__(self, filePath, 'history')
        self.arrays = {}
        self.numInactive = None

    def _precheck(self):
        with open(self.filePath) as check:
            for line in check:
                if line[:3] == 'HIS' or 'active cycles' in line:
                    return
        warning('Unable to find indication of active cycles nor history data '
                'from {}'.format(self.filePath))

    def _postcheck(self):
        if not self.arrays:
            error("No history data found in {}".format(self.filePath))
        if self.numInactive is None:
            error('Unable to acertain the number of inactive cycles')

    def __getitem__(self, key):
        return self.arrays[key]

    def _read(self):
        curKey = None
        scratch = ScratchStorage()
        cycles = None
        indx = 0
        with open(self.filePath) as out:
            for lineNo, line in enumerate(out):
                if not line.strip():
                    continue
                if '=' in line:
                    serpentN = line.split()[0].replace('HIS_', '')
                    curKey = convertVariableName(serpentN)
                    continue
                if 'active' in line:
                    if self.numInactive is None:
                        self.numInactive = indx
                    continue
                if line[0] == ']':
                    data = asfortranarray(scratch.data)
                    self.arrays[curKey] = data
                    cycles = data.shape[0]
                    indx = 0
                    continue
                values = line.split()[1:]  # skip indexing term
                indx += 1
                values = [float(xx) for xx in values]
                if cycles and indx == 1:
                    scratch.allocate((cycles, len(values)))
                scratch[indx - 1] = values

    def _gather_matlab(self, reconvert):
        out = {}
        if reconvert:
            converter = self.ioReconvertName
        else:
            converter = self.ioConvertName
        for key, value in iteritems(self.arrays):
            out[converter(key)] = value
        return out

    def __contains__(self, key):
        """Return ``True`` if key is in :attr:`arrays`, otherwise ``False``"""
        return key in self.arrays

    def __len__(self):
        """Return number of entries in :attr:`arrays`."""
        return len(self.arrays)

    def items(self):
        """Iterate over ``(key, value)`` pairs from :attr:`arrays`"""
        for key, value in iteritems(self.arrays):
            yield key, value

    def __iter__(self):
        """Iterate over keys in :attr:`arrays`"""
        return self.arrays.__iter__()

    @staticmethod
    def ioConvertName(name):
        """Convert a variable name to ``camelCase`` for exporting."""
        return 'his' + name[0].upper() + name[1:]

    @staticmethod
    def ioReconvertName(name):
        """Reconvert a variable name to ``SERPENT_STYLE`` for exporting"""
        return "HIS_" + deconvertVariableName(name)
