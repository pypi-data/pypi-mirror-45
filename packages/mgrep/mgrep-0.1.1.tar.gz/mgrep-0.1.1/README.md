# mgrep

Multiprocess grep (mgrep) is a python grep implementation that utilises all available CPU 
cores to grep multiple files concurrently. For multiple large files it can provide a
20-25x speed increase.

The main purpose of this project is to make James Ponting stop bugging me about it.


## Installation

mgrep is available on pypi, and supports python 3 only. It can be installed as follows:
```
pip3 install mgrep
```

Alternatively, it can be installed in a virtual environment by cloning this repository and
running  `pip install /path/to/this/repo`


## Performance
Example test with 300 files of 25MB each (approx 7.5GB total). Test performed on a 2018
Macbook Pro, YMMV.

* grep:
   ```
   $ time grep "test.*a" * > /tmp/temp1.txt
   grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} "test.*a" * >   103.02s user 2.05s system 99% cpu 1:45.51 total
   ```
* mgrep:
   ```
   $ time mgrep "test.*a" * > /tmp/temp2.txt
   mgrep "test.*a" * > /tmp/temp2.txt  25.59s user 4.84s system 725% cpu 4.195 total
   ```
* Confirm identical output:
   ```
   $ diff /tmp/temp1.txt /tmp/temp2.txt; echo $?
   0
   ```

tl;dr a job that takes ~105 seconds with grep takes ~4 seconds with mgrep


## Options

mgrep supports a handful of options:

* `-i/--ignore-case` (default: false)
    Run a case insensitive match

* `-r/--recursive` (default: false)
   Search files recursively

* `-c/--color` (default: auto)
   Display matched substrings in color

Support for more options can be added on request