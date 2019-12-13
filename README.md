# Materials Studio PBS Script Generator

```
usage: generate_pbs.py [-h] [-w WALLTIME] [-n NODES] [-p PPN] [-q PMEM]
                       [-m MEM] [-e EMAIL] [-x EXECUTABLE] [-d DIRECTORY]
                       [-o OUTPUT]
                       jobfile

Process job options

positional arguments:
  jobfile               Job input filename.

optional arguments:
  -h, --help            show this help message and exit
  -w WALLTIME, --walltime WALLTIME
                        Walltime in HH:MM:SS format. Defaults to 24:00:00
  -n NODES, --nodes NODES
                        Number of nodes to run the job on. Defaults to 1.
  -p PPN, --ppn PPN     Number of processors per node. Defaults to 24.
  -q PMEM, --pmem PMEM  Memory per processor in gb. Defaults to 2gb.
  -m MEM, --mem MEM     Total memory for the job in gb. Defaults to
                        ceil(nodes*ppn*pmem*1.02) (49gb).
  -x EXECUTABLE, --executable EXECUTABLE
                        Script for running the materials studio executable.
                        Defaults to RunCASTEP.sh. Valid choices are
                        ['RunCASTEP.sh', 'RunDMol3.sh'].
  -d DIRECTORY, --directory DIRECTORY
                        Directory containing the Materials Studio job file(s).
                        Defaults to current working directory (/panfs/roc/grou
                        ps/14/msistaff/dunn0404/src/materials_studio_pbs_scrip
                        t)
  -o OUTPUT, --output OUTPUT
                        Name of the PBS job file to write to. Defaults to
                        PBS.txt
```

## Installation

This script requires a python2 version >= 2.7 (for access to argparse). To install the script for use in a Linux system, place it somewhere in your home directory where you store executable scripts (a common choice is to create ~/scripts or ~/bin for this purpose). Then, add the following line to your .bashrc file, replacing the example path with the location of your chosen directory containing generate_pbs.py:

```
export PATH=$PATH:/the/place/where/you/put/the/script/
```


## Example Usage

This script is intended to be run in the Materials Studio job directory to produce a PBS script to run the job on Mesabi. A typical usage on Mesabi, using default values, would be:

```
cd my_job_directory
generate_pbs.py my_ms_jobfile
```

where `my_job_directory` is the directory containing your Materials Studio job, and `my_ms_jobfile` is the name of the Materials Studio job file that you would run as input to e.g. CASTEP. This would generate a PBS script called `PBS.txt` that you would then submit with qsub.
