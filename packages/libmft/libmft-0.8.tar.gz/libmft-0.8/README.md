# libmft

The idea is to have a portable, "fast" way of parsing/reading MFT records.

So far, there is no intention of implementing the ability of writing/editing
MFT records.

## Getting started

### Prerequisites

Python >= 3.6

### Installation

```
pip install libmft
```

### Usage

(TODO document everything in an easy way)

Most of the code is documented and some things I wrote that can be useful are in
the `recipes.py`

## Observations (#TODO document this somewhere else)

Apparently, Microsoft has some mystic rules related to how maintain the MFT records.

Because of that, some things don't make sense when parsing the MFT and some others
are unknown to the community.

### Data not parsed

#### Entries

Entries will not be loaded if they are empty (signature equals to "\x00\x00\x00\x00").

#### Attributes

- First 8 bytes of the VOLUME_INFORMATION attribute

### Interpretation of data

- The EA attribute is not very well understood. There are some trailling stuff and
  mystic alignments that are not confirmed. I'm using a value considering a 8 byte aligment
- The SECURITY_DESCRIPTOR attribute has no implementation of the ACCESS_MASK  object specific
  entries
- The ObjectACE structure needs testing

### Multithread/multiprocessing

I've tried to implement the loading of the file using multiple processes
(multiprocessing, because of the GIL), however, using it the amount of memory
doubled as well as the processing time.

Most likely, the processing time was increased because of the pickling of the data.
The consumption of memory, is not very clear, but probably due to some copying
of the data to multiple processes.

The only way of bypassing that would be to offload part of code to C or
using shared memory. Shared memory in python would be too much trouble (mmap, see
https://blog.schmichael.com/2011/05/15/sharing-python-data-between-processes-using-mmap/) and
if I wanted to write a C library, I would have started that in the first place.

Anyway, if anyone has a suggestion, feel free to let me know.

P.S.: The implementation I used can be seen in the file parallel.py

## TODO/Roadmap?

- Test with windows XP formatted disks (NTFS version < 3)

## Features

### Basic

- [x] MFT Header
- [x] Attribute Header (no named/named)
- [x] Resident Attribute Header
- [x] Non-Resident Attribute Header
- [x] Data runs

### Attributes

- [x] STANDARD_INFORMATION
- [x] ATTRIBUTE_LIST
- [x] FILE_NAME
- [x] OBJECT_ID
- [x] SECURITY_DESCRIPTOR
- [x] VOLUME_NAME
- [x] VOLUME_INFORMATION
- [x] DATA
- [x] INDEX_ROOT
- [ ] INDEX_ALLOCATION (As this is always non-resident, it will not be implemented for now)
- [x] BITMAP
- [x] REPARSE_POINT
- [x] EA_INFORMATION
- [x] EA
- [ ] LOGGED_TOOL_STREAM

## CHANGELOG

### Version 0.8

- Added removed entries to the STANDARD_INFORMATION attribute
- Added removed entries to the FILE_NAME attribute
- Added abstract class for content
- Moved timestamps to its own class
- Removed UID implementation in favor of standard library one
- Added EA and SECURITY_DESCRIPTOR attributes
- Fixed a problem with symbolic links and junction points
- Small fix for reparse point flags
- Changed how attribute headers are represented (API break)
- Code reorganization

### Version 0.7

- Changed the datetime objects to aware objects (UTC timezone)
- Implemented caching (lru_cache) for converting times for performance optimization

### Version 0.5

- Removed the STANDARD_INFORMATION versions and "class ID" fields
- Removed the FILE_NAME "allocated size" and "real size"
- Implemented Datastreams
- Implemented CollationRules
- Updated code for most of the attribute contents
- Updated documentation
- Implemented library configuration in its own class
- Updated code for attribute parsing

## Known problems

- If you try to set the date for a year > 9999, python will fire a Overflow exception.
This is python bound unless we change the datetime module to a third party

## References:

- https://flatcap.org/linux-ntfs/ntfs/concepts/attribute_header.html
- https://github.com/libyal/libfsntfs/blob/master/documentation/New%20Technologies%20File%20System%20(NTFS).asciidoc#mft-entry-header
- https://github.com/sleuthkit/sleuthkit/blob/develop/tsk/fs/tsk_ntfs.h
- http://dubeyko.com/development/FileSystems/NTFS/ntfsdoc.pdf
