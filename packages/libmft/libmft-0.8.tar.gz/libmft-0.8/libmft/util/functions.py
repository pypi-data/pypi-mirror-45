# -*- coding: utf-8 -*-
'''
This module contains auxiliar functions to the library.
'''
import logging
import itertools
from datetime import datetime as _datetime, timedelta as _timedelta, timezone
from collections import Iterable
from functools import lru_cache

from libmft.exceptions import FixUpError

_MOD_LOGGER = logging.getLogger(__name__)
_UTC = timezone.utc
_BASE_DATE_FILETIME64 = _datetime(1601, 1, 1, tzinfo=_UTC)

@lru_cache(512)
def convert_filetime(filetime):
    '''Convert FILETIME64 to datetime object. There is no interpretation of
    timezones. If the encoded format has a timezone, it will be returned as if
    in UTC.

    Args:
        filetime (int) - An int that represents the FILETIME value.

    Returns:
        datetime: The int converted to datetime.
    '''
    #return _datetime(1601, 1, 1) + _timedelta(microseconds=(filetime/10))
    return _BASE_DATE_FILETIME64 + _timedelta(microseconds=(filetime/10))

def get_file_reference(file_ref):
    '''Convert a 32 bits number into the 2 bytes reference and the 6
    bytes sequence number. The return method is a tuple with the
    reference number and the sequence number, in this order.

    Args:
        file_ref (int) - An int that represents the file reference.

    Returns:
        (int, int): A tuple of two ints, where the first is the reference number
            and the second is the sequence number.
    '''
    return (file_ref & 0x0000ffffffffffff, (file_ref & 0xffff000000000000) >> 48)

def apply_fixup_array(bin_view, fx_offset, fx_count, entry_size):
    '''This function reads the fixup array and apply the correct values
    to the underlying binary stream. This function changes the bin_view
    in memory.

    Args:
        bin_view (memoryview of bytearray) - The binary stream
        fx_offset (int) - Offset to the fixup array
        fx_count (int) - Number of elements in the fixup array
        entry_size (int) - Size of the MFT entry
    '''
    fx_array = bin_view[fx_offset:fx_offset+(2 * fx_count)]
    #the array is composed of the signature + substitutions, so fix that
    fx_len = fx_count - 1
    #we can infer the sector size based on the entry size
    sector_size = int(entry_size / fx_len)
    index = 1
    position = (sector_size * index) - 2
    while (position <= entry_size):
        if bin_view[position:position+2].tobytes() == fx_array[:2].tobytes():
            #the replaced part must always match the signature!
            bin_view[position:position+2] = fx_array[index * 2:(index * 2) + 2]
        else:
            _MOD_LOGGER.error("Error applying the fixup array")
            raise FixUpError(f"Signature {fx_array[:2].tobytes()} does not match {bin_view[position:position+2].tobytes()} at offset {position}.")
        index += 1
        position = (sector_size * index) - 2
    _MOD_LOGGER.info("Fix up array applied successfully.")

def flatten(iterable):
    '''This function allows a simple a way to iterate over a "complex" iterable, for example,
    if the input [12, [23], (4, 3), "lkjasddf"], this will return an Iterable that returns
    12, 23, 4, 3 and "lkjasddf".

    Args:
        iterable (Iterable) - A complex iterable that will be flattened

    Returns:
        (Iterable): An Iterable that flattens multiple interables'''
    return itertools.chain.from_iterable(a if isinstance(a,Iterable) and not isinstance(a, str) else [a] for a in iterable)

def get_file_size(file_object):
    '''Returns the size, in bytes, of a file. Expects an object that supports
    seek and tell methods.

    Args:
        file_object (file_object) - The object that represents the file

    Returns:
        (int): size of the file, in bytes'''
    position = file_object.tell()

    file_object.seek(0, 2)
    file_size = file_object.tell()
    file_object.seek(position, 0)

    return file_size
