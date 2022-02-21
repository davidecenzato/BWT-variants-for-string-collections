#!/usr/bin/python

import os, sys, subprocess, signal, argparse, datetime, time

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-f', help='custom fasta file name (def. file.fasta)', default="file.fasta", type=str)
	parser.add_argument('--edit', help='compute edit distance on custom input in addition to Hamming distance and number of runs (def. False)', action='store_true')
	parser.add_argument('--noeditlong', help='compute everything but edit distances on long sequences (def. False)', action='store_true')
	parser.add_argument('--all', help='compute distances and number of runs for all datasets of the paper (def. False)', action='store_true')
	args = parser.parse_args()

	dirname = os.path.dirname(os.path.abspath(__file__))
	logdir_path = os.path.join(dirname,"logs/")
	log_path = os.path.join(logdir_path, datetime.datetime.now().strftime("%Y%m%d") + "/")
	logfile_name = log_path + "dist_run_log.txt"
	data_path = os.path.join(dirname,"data/")
	dataset_list = ["SARSCov2short.fasta -r -H","SARSCov2short_small.fasta -r -H -e",
					"SimonDivreads.fasta -r -H","SimonDivreads_small.fasta -r -H -e",
					"16SrRNAshort.fasta  -r -H","16SrRNAshort_small.fasta  -r -H -e",
					"InfluenzaA.fasta  -r -H","InfluenzaA_small.fasta -r -H -e",
					"SARSCov2long.fasta -r -H","SARSCov2long_small.fasta -r -H -e",
					"16SrRNAlong.fasta  -r -H","16SrRNAlong_small.fasta -r -H -e",
					"CandidaAuris.fasta  -r -H","CandidaAuris_small.fasta -r -H -e",
					"SARSCov2genomes.fasta  -r -H","SARSCov2genomes_small.fasta -r -H -e"]
	if args.noeditlong:
		dataset_list = ["SARSCov2short.fasta -r -H","SARSCov2short_small.fasta -r -H -e",
					    "SimonDivreads.fasta -r -H","SimonDivreads_small.fasta -r -H -e",
					    "16SrRNAshort.fasta  -r -H","16SrRNAshort_small.fasta  -r -H -e",
					    "InfluenzaA.fasta  -r -H","InfluenzaA_small.fasta -r -H -e",
					    "SARSCov2long.fasta -r -H","SARSCov2long_small.fasta -r -H",
					    "16SrRNAlong.fasta  -r -H","16SrRNAlong_small.fasta -r -H",
					    "CandidaAuris.fasta  -r -H","CandidaAuris_small.fasta -r -H",
					    "SARSCov2genomes.fasta  -r -H","SARSCov2genomes_small.fasta -r -H"]

	# create the logdir if not exists
	if not os.path.exists(log_path):
		os.makedirs(log_path)

	command = ""
	start = time.time()
	# open logfile
	with open(logfile_name,"a") as logfile: 

		if args.all:
			for i in range(0,len(dataset_list)):
				command = "python3 compute_run_dist.py -f " + dataset_list[i] 
				# execute command
				if(execute_command(command,logfile,logfile_name)!=True):
					exit(1)
					
			print("All distances and number of runs were sucessfully generated, elapsed time: {0:.4f}".format(time.time()-start))

		else:
			command = "python3 python3 compute_run_dist.py -f " + args.f + " -r -H"
			if args.edit: command + " -e"
			print(command)
			if(execute_command(command,logfile,logfile_name)!=True):
				exit(1)
			print("All distance and number of runs " + args.f + " were sucessfully generated, elapsed time: {0:.4f}".format(time.time()-start))


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