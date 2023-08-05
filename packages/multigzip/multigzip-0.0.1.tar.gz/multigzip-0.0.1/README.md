# Multi GZip

This package is a port of the Python2 gzip implementation with the goal of
providing multi-member gzip support. Currently Python3's gzip implementation
supports reading multi-member gzip files as a single stream, but does not 
provide the ability to read or write one member at a time. This is useful
for iterating over the members of a gzip file in e.g. WARC files.

## Usage Example

```python
from multigzip import GzipFile

with GzipFile(filename='tests.txt.gz', mode='wb') as f:
    f.write_member(b'Hello world 1')
    f.write_member(b'Hello world 2')
    f.write_member(b'Hello world 3')

with GzipFile(filename='tests.txt.gz', mode='r') as f:
    # Note that read() returns a file-like object
    # this is unchanged vs the `gzip2` module ported
    # from warc
    print(f.read_member().read())
    print(f.read_member().read())
    print(f.read_member().read())

```

### Supports Python3 Only
