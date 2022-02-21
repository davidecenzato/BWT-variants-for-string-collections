import timeit, sys, math, argparse, os, datetime, subprocess, signal, time, replace, shutil

def main():

	dirname = os.path.dirname(os.path.abspath(__file__))
	data_folder = os.path.join(dirname,"data/")
	logdir_path = os.path.join(dirname,"logs/")
	log_path = os.path.join(logdir_path, datetime.datetime.now().strftime("%Y%m%d") + "/")
	logfile_name = log_path + "download_gen_fasta.txt"
	fastq_dump = "fastq-dump"
	prefetch = "prefetch"

	# create the logdir if not exists
	if not os.path.exists(log_path):
		os.makedirs(log_path)

	#for sra_id in ["SRR12038588", "ERR1019034", "SRR10391186", "SRR10391186",
	#               "SRR7507278"]:
	#	print ("Currently downloading: " + sra_id)
	#	command = prefetch + " " + sra_id
	#	print("The command used was: " + prefetch)
	#	if(execute_command(command,logfile,logfile_name)!=True):
	#		exit(1)

	with open(logfile_name,"a") as logfile:
		# download and create big and small data set for SARSCoV2short 
		sra_id = "SRR12038588"
		print ("Generating SARSCoV2short fasta with sra: " + sra_id)
		command = "{fastq_dump} --outdir {outdir} --skip-technical --fasta 0".format(fastq_dump = fastq_dump, outdir = data_folder) 
		command += " --defline-seq '@$ac.$si.1 $si length=$rl' " + str(sra_id)
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		# create big and small data set
		command = '''head -n 1000000 {file} > {output}'''.format(file=data_folder + sra_id + ".fasta", output=data_folder + "SARSCov2short.fasta")
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command_small = '''head -n 10000 {file} > {output}'''.format(file=data_folder +sra_id+".fasta", output=data_folder + "SARSCov2short_small.fasta")
		if(execute_command(command_small,logfile,logfile_name)!=True):
			exit(1)
		os.remove(data_folder+"{file}".format(file=sra_id+".fasta"))
		# download and create big and small data set for SimonsDiversityreads
		sra_id = "ERR1019034"
		print ("Generating SimonDivreads fasta with sra: " + sra_id)
		command = "{fastq_dump} --outdir {outdir} --skip-technical --fasta 0".format(fastq_dump = fastq_dump, outdir = data_folder) 
		command += " --defline-seq '@$ac.$si' --split-files -N 87345775 -X 87845776 " + str(sra_id)
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = "seqkit grep -w 0 {input} -f {headers} > {output}".format(input=data_folder+sra_id+"_1.fasta", headers=data_folder+"SimonDivreads_ids.txt",
		                                                                    output=data_folder+"SimonDivreads.fasta")
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command_small = '''head -n 10000 {file} > {output}'''.format(file=data_folder +  "SimonDivreads.fasta", output=data_folder + "SimonDivreads_small.fasta")
		if(execute_command(command_small,logfile,logfile_name)!=True):
			exit(1)
		os.remove(data_folder+"{file}".format(file=sra_id+"_1.fasta"))
		os.remove(data_folder+"{file}".format(file=sra_id+"_2.fasta")) 
		# download and create big and small data set for 16SrRNAshort dataset
		sra_id = "SRR10391186"
		print ("Generating 16SrRNAshort fasta with sra: " + sra_id)
		command = "{fastq_dump} --outdir {outdir} --skip-technical --fasta 0".format(fastq_dump = fastq_dump, outdir = data_folder) 
		command += " --defline-seq '@$ac.$si.$ri' --split-spot " + str(sra_id)
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = "seqkit grep -w 0 {input} -f {headers} > {output}".format(input=data_folder+sra_id+".fasta", headers=data_folder+"16SrRNAshort_ids.txt",
				                                                            output=data_folder+"16SrRNAshort.fasta")
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = '''head -n 10000 {file} > {output}'''.format(file=data_folder +  "16SrRNAshort.fasta", output=data_folder + "16SrRNAshort_small.fasta")
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		os.remove(data_folder+"{file}".format(file=sra_id+".fasta"))
		# download and create big and small data set for InfluenzaA
		sra_id = "SRR1757953"
		print ("Generating InfluenzaA fasta with sra: " + sra_id)
		command = "{fastq_dump} --outdir {outdir} --skip-technical --fasta 0".format(fastq_dump = fastq_dump, outdir = data_folder) 
		command += " --defline-seq '@$ac.$si.$ri' --split-spot " + str(sra_id)
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = "seqkit grep -w 0 {input} -f {headers} > {output}".format(input=data_folder+sra_id+".fasta", headers=data_folder+"InfluenzaA_ids.txt",
				                                                            output=data_folder+"InfluenzaA.fasta")
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = '''head -n 10000 {file} > {output}'''.format(file=data_folder +  "InfluenzaA.fasta", output=data_folder + "InfluenzaA_small.fasta")
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		os.remove(data_folder+"{file}".format(file=sra_id+".fasta"))
		# download and create big and small dataset for SARSCov2long SRR16287139
		print("Download and compute big and small data set for SARSCov2long")
		print("Downloading raw sequences...")
		command = "wget https://sra-pub-sars-cov2.s3.amazonaws.com/sra-src/SRR16287139/demultiplex.bc1021_BAK8B_OA--bc1021_BAK8B_OA.hifi_reads.fastq.gz.1"
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		print("Done!")
		os.rename("demultiplex.bc1021_BAK8B_OA--bc1021_BAK8B_OA.hifi_reads.fastq.gz.1","hifi_reads.fastq.gz")
		command = "gzip -d hifi_reads.fastq.gz"
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = "seqkit fq2fa hifi_reads.fastq > "+data_folder+"SARSCov2longRAW.fasta"
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		os.remove("hifi_reads.fastq")
		command = "seqkit grep -w 0 {input} -f {headers} > {output}".format(input=data_folder+"SARSCov2longRAW.fasta", headers=data_folder+"SARSCov2long_ids.txt",
				                                                            output=data_folder+"SARSCov2long.fasta")
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command_small = '''head -n 3000 {file} > {output}'''.format(file=data_folder+"SARSCov2long.fasta", output=data_folder + "SARSCov2long_small.fasta")
		if(execute_command(command_small,logfile,logfile_name)!=True):
			exit(1)
		os.remove(data_folder+"{file}".format(file="SARSCov2longRAW.fasta"))
		# download and create big and small dataset for 16SrRNAlong 
		print("Download and compute big and small data set for 16SrRNAlong")
		print("Downloading raw sequences...")
		command = "wget https://drive5.com/opti_paper/supp_data.tar.gz"
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		print("Done!")
		command = "gzip -d supp_data.tar.gz"
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		# create the logdir if not exists
		if not os.path.exists(os.path.join(dirname,"temp/")):
			os.makedirs(os.path.join(dirname,"temp/"))
		command = "tar -C ./temp/ -xvf supp_data.tar"
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		os.remove(dirname + "/supp_data.tar")
		command = "seqkit head -n 20000 -w 0 {file} > {output}".format(file=os.path.join(dirname,"temp/")+"data/hiq_fl.fa", output=data_folder+"16SrRNAlong.fasta")
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		shutil.rmtree(os.path.join(dirname,"temp/"))
		command = "seqkit head -n 1500 -w 0 {file} > {output}".format(file=data_folder + "16SrRNAlong.fasta", output=data_folder + "16SrRNAlong_small.fasta")
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		# download and create big and small data set for CandidaAurisreads
		sra_id = "SRR7507278"
		print ("Generating CandidaAuris fasta with sra: " + sra_id)
		command = "{fastq_dump} --outdir {outdir} --skip-technical --fasta 0".format(fastq_dump = fastq_dump, outdir = data_folder) 
		command += " --defline-seq '@$ac.$si' " + str(sra_id)
		print(command)
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = "seqkit grep -w 0 {input} -f {headers} > {output}".format(input=data_folder+sra_id+".fasta", headers=data_folder+"CandidaAuris_ids.txt",
				                                                            output=data_folder+"CandidaAuris.fasta")
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		command = '''head -n 3000 {file} > {output}'''.format(file=data_folder +  "CandidaAuris.fasta", output=data_folder + "CandidaAuris_small.fasta")
		if(execute_command(command,logfile,logfile_name)!=True):
			exit(1)
		os.remove(data_folder+"{file}".format(file=sra_id+".fasta"))

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