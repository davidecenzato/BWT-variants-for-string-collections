#!/usr/bin/python

import timeit, sys, math, argparse, os, sys, datetime, subprocess, signal, time, decimal, Levenshtein, statistics, replace

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-f', help='base BWT variants file path (def. file.fasta)', default="file.fasta", type=str)
	parser.add_argument('-r', help='compute number of runs and average runlength (def. False)', action='store_true')
	parser.add_argument('-H', help='compute Hamming distance on separator based BWT variants (def. False)', action='store_true')
	parser.add_argument('-e', help='compute edit distance on small datasets (def. False)', action='store_true')
	args = parser.parse_args()

	dirname = os.path.dirname(os.path.abspath(__file__))
	logdir_path = os.path.join(dirname,"logs/")
	log_path = os.path.join(logdir_path, datetime.datetime.now().strftime("%Y%m%d") + "/")
	logfile_name = log_path + "res_log.txt"
	res_path = os.path.join(dirname,"results/")
	BWTs_path = os.path.join(dirname,"BWTvar/")
	csv_Hamming_dist = os.path.join(res_path, args.f + "_Hamming_dist_" + datetime.datetime.now().strftime("%Y%m%d") + ".csv")
	csv_edit_dist = os.path.join(res_path, args.f + "_edit_dist_" + datetime.datetime.now().strftime("%Y%m%d") + ".csv")
	csv_run_stat = os.path.join(res_path, args.f + "_run_stat_" + datetime.datetime.now().strftime("%Y%m%d") + ".csv")

	# create the logdir if not exists
	if not os.path.exists(log_path):
		os.makedirs(log_path)

	# create the resdir if not exists
	if not os.path.exists(res_path):
		os.makedirs(res_path)

	bwt_paths = [BWTs_path + args.f + ".eBWT", BWTs_path + args.f+".dolEBWT",
	             BWTs_path + args.f + ".mdolBWT", BWTs_path + args.f +".colexBWT",
	             BWTs_path + args.f + ".concBWT"]

	for bwt in bwt_paths:
		# check if files exist
		if not os.path.isfile(bwt):
			print("File path {} does not exist. Exiting...".format(bwt))
			sys.exit()
		else:
			print(bwt + str(" found!"))

	command = ""
	start = time.time()
	# open logfile
	with open(logfile_name,"a") as logfile:
		# compute run stats
		if args.r:
			print("Sending summary to: " + csv_run_stat)
			with open(csv_run_stat,"w") as csv_file:
				csv_file.write("BWTvariant,r,n/r\n")
				for bwt in bwt_paths:
					length,runs,ratio = Run_stats(bwt)
					csv_file.write(bwt.split('.')[-1] + "," + str(runs) + "," + str(ratio) + "\n")
		# compute Hamming distance			
		if args.H:
			Hamming_dists = []
			norm_Hamming_dists = []
			print("Sending summary to: " + csv_Hamming_dist)
			with open(csv_Hamming_dist,"w") as csv_file:
				csv_file.write(",dolEBWT,mdolBWT,colexBWT,concBWT\n")
				bwt1 = ""; bwt2 = "";
				for k1 in range(1,len(bwt_paths)-1):
					path1 = bwt_paths[k1]
					with open(path1, 'rb') as bf1:
						bwt1 = bf1.read().decode()
					for k2 in range(k1+1,len(bwt_paths)):
						path2 = bwt_paths[k2]
						with open(path2, 'rb') as bf2:
							bwt2 = bf2.read().decode()
						# compute distances
						dis, seen = Hamming_distance(bwt1,bwt2) 
						norm = decimal.Decimal(float(dis)/seen)
						Hamming_dists.append(dis)
						norm_Hamming_dists.append(norm)
				del bwt1; del bwt2;
				# write results to file
				csv_file.write("dolEBWT,0," + str(Hamming_dists[0]) + "," + str(Hamming_dists[1]) + "," +
				               str(Hamming_dists[2]) + "\n")
				csv_file.write("mdolBWT," + str(norm_Hamming_dists[0]) + ",0," + str(Hamming_dists[3]) + "," +
				               str(Hamming_dists[4]) + "\n")
				csv_file.write("colexBWT," + str(norm_Hamming_dists[1]) + "," + str(norm_Hamming_dists[3]) + ",0," +
				        	   str(Hamming_dists[5]) + "\n")
				csv_file.write("concBWT," + str(norm_Hamming_dists[2]) + "," + str(norm_Hamming_dists[4]) + "," +
				        	   str(norm_Hamming_dists[5]) + ",0\n")
			del Hamming_dists; del norm_Hamming_dists;
		# compute edit distance on small data set			
		if args.e:
			edit_dists = []
			norm_edit_dists = []
			bwt1 = ""; bwt2 = "";
			print("Sending summary to: " + csv_edit_dist)
			with open(csv_edit_dist,"w") as csv_file:
				csv_file.write(",eBWT,dolEBWT,mdolBWT,colexBWT,concBWT\n")
				for k1 in range(len(bwt_paths)-1):
					path1 = bwt_paths[k1]
					with open(path1, 'rb') as bf1:
						bwt1 = bf1.read().decode()
					for k2 in range(k1+1,len(bwt_paths)):
						path2 = bwt_paths[k2]
						with open(path2, 'rb') as bf2:
							bwt2 = bf2.read().decode()
						dist = Levenshtein.distance(bwt1, bwt2)
						norm = decimal.Decimal(float(dist)/max(len(bwt1),len(bwt2)))
						edit_dists.append(dist)
						norm_edit_dists.append(norm)
				# write results to file
				csv_file.write("eBWT,0," + str(edit_dists[0]) + "," + str(edit_dists[1]) + "," +
				               str(edit_dists[2]) + "," + str(edit_dists[3]) + "\n")
				csv_file.write("dolEBWT," + str(norm_edit_dists[0]) + ",0," + str(edit_dists[4]) + "," +
				               str(edit_dists[5]) + "," + str(edit_dists[6]) +"\n")
				csv_file.write("mdolBWT," + str(norm_edit_dists[1]) + "," + str(norm_edit_dists[4]) + ",0," +
				        	   str(edit_dists[7]) + "," + str(edit_dists[8]) + "\n")
				csv_file.write("colexBWT," + str(norm_edit_dists[2]) + "," + str(norm_edit_dists[5]) + "," +
				        	   str(norm_edit_dists[7]) + ",0," + str(edit_dists[9]) + "\n")
				csv_file.write("concBWT," + str(norm_edit_dists[3]) + "," + str(norm_edit_dists[6]) + "," +
				        	   str(norm_edit_dists[8]) + "," + str(norm_edit_dists[9]) + ",0\n")
			del edit_dists; del norm_edit_dists;


def Hamming_distance(seq1, seq2):
	dist = seen = 0
	len1 = len(seq1)
	len2 = len(seq2)
	flag = False 
	if len1 != len2:
		if abs(len1 - len2) != 1:
			print(abs(len1 - len2))
			print(len1)
			print(len2)
			print("Error! BWT error length... exiting.")
			exit(1)
		if len1 > len2:
			dist = Levenshtein.hamming(seq1[1:],seq2)
		else:
			dist = Levenshtein.hamming(seq1,seq2[1:])
		seen = min(len1,len2)
	else:
		if len1 != len2:
			print("Error! sequences with different lengths... exiting.")
			exit(1)
		dist = Levenshtein.hamming(seq1,seq2)
		seen = len1

	return dist, seen

def Run_stats(bwt_path):
	length = 1
	runs = 1
	# read BWT from file
	with open(bwt_path, 'rb') as bf:
		prev = bf.read(1).decode();
		while True:
			current = bf.read(1).decode();
			# break when reach EOF
			if not current:
				break
			length += 1
			if prev != current:
				runs += 1
			prev = current

	return length, runs, decimal.Decimal(float(length)/runs)

def comma(number):
    return ("{:,}".format(number))

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