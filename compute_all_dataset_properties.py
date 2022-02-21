#!/usr/bin/python

import timeit, sys, math, argparse, os, sys, datetime, subprocess, signal, time, decimal

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-f', help='custom fasta file name (def. file.fasta)', default="file.fasta", type=str)
	parser.add_argument('--all', help='compute properties for all datasets in the paper (def. False)', action='store_true')
	args = parser.parse_args()

	dirname = os.path.dirname(os.path.abspath(__file__))
	#logdir_path = os.path.join(dirname,"logs/")
	log_path = os.path.join(dirname,"results/")
	#log_path = os.path.join(logdir_path, datetime.datetime.now().strftime("%Y%m%d") + "/")
	logfile_name = log_path + "dataset_properties.txt"
	data_path = os.path.join(dirname,"data/")
	dataset_list = ["SARSCov2short.fasta","SARSCov2short_small.fasta","SimonDivreads.fasta","SimonDivreads_small.fasta",
					"16SrRNAshort.fasta","16SrRNAshort_small.fasta","InfluenzaA.fasta","InfluenzaA_small.fasta",
					"SARSCov2long.fasta","SARSCov2long_small.fasta","16SrRNAlong.fasta","16SrRNAlong_small.fasta",
					"CandidaAuris.fasta","CandidaAuris_small.fasta","SARSCov2genomes.fasta","SARSCov2genomes_small.fasta"]

	# create the logdir if not exists
	if not os.path.exists(log_path):
		os.makedirs(log_path)

	command = ""
	start = time.time()
	# open logfile
	with open(logfile_name,"a") as logfile: 

		if args.all:
			for i in range(0,len(dataset_list)):
				command = "python3 compute_data_properties.py " + data_path + dataset_list[i]
				print(command)
				if(execute_command(command,logfile,logfile_name)!=True):
					exit(1)
		else:
			command = "python3 compute_data_properties.py " + data_path + args.f 
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