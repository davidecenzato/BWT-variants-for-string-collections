#!/usr/bin/python

## Script for generating all BWT variants from the data sets

import os, sys, subprocess, signal, glob, argparse, datetime, time

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-f', help='custom fasta file name (def. file.fasta)', default="file.fasta", type=str)
	parser.add_argument('--short', help='input fasta file contains short reads (def. False)', action='store_true')
	parser.add_argument('--all', help='build all BWT variants of the paper (def. False)', action='store_true')
	parser.add_argument('--remove_all', help='remove all BWT variants (def. False)', action='store_true')
	args = parser.parse_args()

	dirname = os.path.dirname(os.path.abspath(__file__))
	logdir_path = os.path.join(dirname,"logs/")
	log_path = os.path.join(logdir_path, datetime.datetime.now().strftime("%Y%m%d") + "/")
	logfile_name = log_path + "bwtvargen.log"
	data_path = os.path.join(dirname,"data/")
	BWTvar_path = os.path.join(dirname,"BWTvar/")
	dataset_list = ["SARSCov2short.fasta -r","SARSCov2short_small.fasta -r","SimonDivreads.fasta -r","SimonDivreads_small.fasta -r",
					"16SrRNAshort.fasta -r","16SrRNAshort_small.fasta -r","InfluenzaA.fasta -r","InfluenzaA_small.fasta -r",
					"SARSCov2long.fasta -r","SARSCov2long_small.fasta -r","16SrRNAlong.fasta","16SrRNAlong_small.fasta",
					"CandidaAuris.fasta -r","CandidaAuris_small.fasta -r","SARSCov2genomes.fasta","SARSCov2genomes_small.fasta"]

	# create the logdir if not exists
	if not os.path.exists(log_path):
		os.makedirs(log_path)

	command = ""
	start = time.time()
	# open logfile
	with open(logfile_name,"a") as logfile: 

		if args.remove_all:
			for filename in glob.glob(BWTvar_path):
				os.remove(filename)
		else:
			if args.all:
				for i in range(0,len(dataset_list)):
					command = "python3 compute_bwt_variants.py -f " + dataset_list[i]
					print(command)
					if(execute_command(command,logfile,logfile_name)!=True):
						exit(1)
			else:
				command = "python3 compute_bwt_variants.py -f " + args.f 
				if args.short: command + " -r"
				print(command)
				if(execute_command(command,logfile,logfile_name)!=True):
					exit(1)


# execute command: return True is everything OK, False otherwise
def execute_command(command,logfile,logfile_name,env=None):
  try:
	#subprocess.run(command.split(),stdout=logfile,stderr=logfile,check=True,env=env)
    subprocess.check_call(command,stdout=logfile,stderr=logfile,env=env,shell=True)
  except subprocess.CalledProcessError:
    print("Error executing command line:")
    print("\t"+ command)
    print("Check log file: " + logfile_name)
    return False
  return True


if __name__ == '__main__':
    main()