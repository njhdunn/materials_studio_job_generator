#! /usr/bin/env python
import argparse
import math
import os

def total_mem(nodes, ppn, pmem):
	return int(math.ceil(pmem*nodes*ppn*1.02))

DEFAULT_WALLTIME="24:00:00"
DEFAULT_NODES=1
DEFAULT_PPN=24
DEFAULT_PMEM=2
DEFAULT_MEM= total_mem(nodes=DEFAULT_NODES, ppn=DEFAULT_PPN, pmem=DEFAULT_PMEM)
DEFAULT_OUTPUT="PBS.txt"

VALID_EXES = [ "RunCASTEP.sh", "RunDMol3.sh"]
DEFAULT_EXE=VALID_EXES[0]

WORKING_DIR = os.getcwd()

pbs_template_string = ("#!/bin/bash -l\n"
"#PBS -l walltime={WALLTIME},pmem={PMEM}gb,mem={MEM}gb,nodes={NODES}:ppn={PPN}\n"
"#PBS -m abe\n"
"module load materialsstudio/2018\n"
"export DSD_MachineList=$PBS_NODEFILE\n"
"export LD_LIBRARY_PATH=/lib64:/usr/lib64:$LD_LIBRARY_PATH\n"
"cd {JOB_DIRECTORY}\n"
"{EXECUTABLE} -np {NP} {JOB_FILE}")


parser = argparse.ArgumentParser(description="Process job options")

# Mandatory arguments
parser.add_argument("jobfile", type=str, action="store", help="Job input filename.")

# Optional arguments with default fallbacks
parser.add_argument("-w", "--walltime", type=str, default=DEFAULT_WALLTIME,
			action="store", help="Walltime in HH:MM:SS format. Defaults to {0}".format(DEFAULT_WALLTIME))
parser.add_argument("-n", "--nodes", type=int, action="store", default=DEFAULT_NODES, 
			help="Number of nodes to run the job on. Defaults to {0}.".format(DEFAULT_NODES))
parser.add_argument("-p", "--ppn", type=int, action="store", default=DEFAULT_PPN,
			help="Number of processors per node. Defaults to {0}.".format(DEFAULT_PPN))
parser.add_argument("-q", "--pmem", type=int, action="store",
			help="Memory per processor in gb. Defaults to 2gb.".format(DEFAULT_PMEM))
parser.add_argument("-m", "--mem", type=int, action="store",
			help="Total memory for the job in gb. Defaults to ceil(nodes*ppn*pmem*1.02) ({0}gb).".format(DEFAULT_MEM))
parser.add_argument("-x", "--executable", type=str, action="store", default=DEFAULT_EXE,
			help=("Script for running the materials studio executable. Defaults to {0}."
				" Valid choices are {1}.").format(DEFAULT_EXE, VALID_EXES))
parser.add_argument("-d", "--directory", type=str, action="store", default=WORKING_DIR,
			help=("Directory containing the Materials Studio job file(s)."
				" Defaults to current working directory ({0})").format(WORKING_DIR))
parser.add_argument("-o", "--output", type=str, action="store", default=DEFAULT_OUTPUT,
			help=("Name of the PBS job file to write to. Defaults to {0}".format(DEFAULT_OUTPUT)))

args = parser.parse_args()


## Calculate derivative values where necessary

total_nodes = args.ppn*args.nodes

if args.pmem != None:
	final_pmem = args.pmem
else:
	final_pmem = DEFAULT_PMEM


if args.mem != None:
	total_mem = args.mem
else:
	total_mem = total_mem(nodes=args.nodes, ppn=args.ppn, pmem=final_pmem)


jobfile = "{0}.xsd".format(args.jobfile )



## Basic error checking

if args.ppn > 24:
	print "ERROR: Requesting more than 24 processors per node:"
	print "PPN={0}".format(args.ppn)
	exit(1)

if args.executable not in VALID_EXES:
	print "ERROR: Requested script {0} not a valid choice for this script.".format(args.executable)
	print "Valid choices are: {0}".format(VALID_EXES)
	exit(1)

if total_mem > 1024:
	print "ERROR: Requested job would ask for >1TB of memory ({0}gb).".format(total_mem)
	print "There is no queue where this job would run on mesabi."
	exit(1)

if not os.path.isfile(jobfile):
	print "ERROR: File \'{0}\' not found in specified directory {1}".format(jobfile, args.directory)
	exit(1)

## Format output string

pbs_string = pbs_template_string.replace("{WALLTIME}", args.walltime)
pbs_string = pbs_string.replace("{NODES}", str(args.nodes))
pbs_string = pbs_string.replace("{PPN}", str(args.ppn))
pbs_string = pbs_string.replace("{NP}", str(total_nodes))
pbs_string = pbs_string.replace("{MEM}", str(total_mem))
pbs_string = pbs_string.replace("{PMEM}", str(final_pmem))
pbs_string = pbs_string.replace("{EXECUTABLE}", args.executable)
pbs_string = pbs_string.replace("{JOB_FILE}", args.jobfile)
pbs_string = pbs_string.replace("{JOB_DIRECTORY}", args.directory)

outfile = open(args.output, "w")
outfile.write(pbs_string)
outfile.close()
print "Results written to {0}".format(args.output)


