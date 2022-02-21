#!/usr/bin/python

import timeit, sys, math, argparse, os, sys, datetime, subprocess, signal, time, replace, shutil

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-f', help='fasta file path (def. file.fasta)', default="file.fasta", type=str)
	parser.add_argument('-r', help='short reads data (def. False)', action='store_true')
	args = parser.parse_args()

	dirname = os.path.dirname(os.path.abspath(__file__))
	logdir_path = os.path.join(dirname,"logs/")
	log_path = os.path.join(logdir_path, datetime.datetime.now().strftime("%Y%m%d") + "/")
	logfile_name = log_path + "bwtvarcomp_log.txt"
	BWTvar_path = os.path.join(dirname,"BWTvar/")
	data_path = os.path.join(dirname,"data/")

	# create the logdir if not exists
	if not os.path.exists(log_path):
		os.makedirs(log_path)

	# create the bwtvariants dir if not exists
	if not os.path.exists(BWTvar_path):
		os.makedirs(BWTvar_path)
    
	rope_path = os.path.join(dirname,"ropebwt2/ropebwt2")
	big_path = os.path.join(dirname,"bigbwt/bigbwt")
	ebwt_path = os.path.join(dirname,"pfpebwt/build/pfpebwt")

	# check if datasets exist
	if not os.path.isfile(data_path + args.f):
		print("File path {} does not exist. Exiting...".format(data_path + args.f))
		sys.exit()
	else:
		print(data_path + args.f + str(" found!"))

	command = ""
	start = time.time()
	# open logfile
	with open(logfile_name,"a") as logfile: 
		# generate mdolBWT BWT
		command = rope_path + " -o {output} -R {input}".format(input = data_path+args.f, output = BWTvar_path + args.f + ".mdolBWT")
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = '''truncate -s -1 {input}'''.format(input = BWTvar_path + args.f + ".mdolBWT")
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		# generate concBWT rlo BWT
		command = rope_path + " -o {output} -R -s {input}".format(input = data_path + args.f, output = BWTvar_path + args.f + ".colexBWT")
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = '''truncate -s -1 {input}'''.format(input = BWTvar_path + args.f + ".colexBWT")
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		# generate the eBWT
		if args.r:
			command = ebwt_path + " {input} -w 10 -p 10 -n 3 --reads --period".format(input = data_path + args.f)
		else:
			command = ebwt_path + " {input} -w 10 -p 100".format(input = data_path + args.f)
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		os.remove(data_path + args.f + ".ebwt.r")
		os.remove(data_path + args.f + ".I")
		os.remove(data_path + args.f + ".log")
		if os.path.isfile(data_path + args.f + ".filtered"):
			if(os.path.getsize(data_path + args.f + ".filtered") > 0):
				print(str(os.path.getsize(data_path + args.f + ".filtered")) + " reads filtered")
			else:
				os.remove(data_path + args.f + ".filtered")
		shutil.move(data_path + args.f + ".ebwt", BWTvar_path + args.f + ".eBWT")
		# generate dolEBWT
		command = "seqkit replace -sp '$' -r '$' -w 0 {input} >> {temp}".format(input = data_path + args.f, temp = BWTvar_path + args.f +".doll")
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		if args.r:
			command = ebwt_path + " {input} -w 10 -p 10 -n 3 --reads --period".format(input = BWTvar_path + args.f +".doll")
		else:
			command = ebwt_path + " {input} -w 10 -p 100".format(input = BWTvar_path + args.f +".doll")
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		os.remove(BWTvar_path + args.f + ".doll.ebwt.r")
		os.remove(BWTvar_path + args.f + ".doll.I")
		os.remove(BWTvar_path + args.f + ".doll.log")
		if os.path.isfile(BWTvar_path + args.f + ".doll.filtered"):
			if(os.path.getsize(BWTvar_path + args.f + ".doll.filtered") > 0):
				print(str(os.path.getsize(BWTvar_path + args.f + ".doll.filtered")) + " reads filtered")
			else:
				os.remove(BWTvar_path + args.f + ".doll.filtered")
		os.remove(BWTvar_path + args.f + ".doll")
		os.rename(BWTvar_path + args.f + ".doll.ebwt",BWTvar_path + args.f + ".dolEBWT")
		# generate concBWT
		command = '''grep -v ">" {input} > {temp}'''.format(input = data_path + args.f, temp = BWTvar_path + args.f + ".plain")
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = big_path + " " + BWTvar_path + args.f + ".plain"
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		os.remove(BWTvar_path + args.f + ".plain.log")
		os.remove(BWTvar_path + args.f + ".plain")
		os.rename(BWTvar_path + args.f + ".plain.bwt",BWTvar_path + args.f +".concBWT")
		replace.replace_char(BWTvar_path + args.f +".concBWT","newline","$")
		replace.replace_char(BWTvar_path + args.f +".concBWT","zero","#")
	print("All BWT variants for " + args.f + " were sucessfully generated, elapsed time: {0:.4f}".format(time.time()-start))


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