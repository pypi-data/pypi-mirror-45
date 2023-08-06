# mgrep

Multiprocess grep (mgrep) is a python grep implementation that utilises all multiple CPU 
cores to grep many files concurrently. For large sets of files it can provide a 20-25x 
speed increase.

The main purpose of this project is to make James stop bugging me about it.


## Installation

mgrep is available on PyPi and requires python 3. It can be installed as follows:

    pip3 install mgrep

Alternatively, it can be installed by cloning this repository and  running  
`pip install /path/to/this/repo`


## Usage

mgrep can be used just like grep:

    mgrep "^some.*pattern$" *.log
    mgrep -r "test" /path/to/some/folder
    mgrep -i "case insensitive search" *.log

It currently supports a subset of standard grep flags. Receiving input via stdin (piping 
or redirection) is not currently supported, since mgrep offers far fewer advantages over
plain grep when working on a single input stream.


## Performance

Example test with 300 files of 25MB each (approx 7.5GB total). Test performed on a 2018
Macbook Pro, YMMV.

* grep:

        $ time grep "test.*a" * > /tmp/temp1.txt
        grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} "test.*a" * >   103.02s user 2.05s system 99% cpu 1:45.51 total

* mgrep:

        $ time mgrep "test.*a" * > /tmp/temp2.txt
        mgrep "test.*a" * > /tmp/temp2.txt  25.59s user 4.84s system 725% cpu 4.195 total

* Confirm identical output:

        $ diff /tmp/temp1.txt /tmp/temp2.txt; echo $?
        0

tl;dr a job that takes ~105 seconds with grep takes ~4 seconds with mgrep.

Note: In order to print results from concurrent greps in the correct order mgrep must hold 
all matched lines in memory. This means that unlike regular grep, the memory used by mgrep 
increases as the number of matched lines increases. In the above example 1,746,969 lines 
were matched (an extreme case) and roughly 1GB of memory was used.


## Options

mgrep supports a handful of options:

* `-i/--ignore-case` (default: false)
    Run a case insensitive match

* `-r/--recursive` (default: false)
   Search files recursively

* `--color` (default: auto)
   Display matched substrings in color

* `--version`
   Display mgrep version

Support for more options can be added on request