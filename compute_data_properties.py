#!/usr/bin/python

# script for computing the properties of all datasets in the paper

import sys, itertools, math, argparse, time, numpy

DNA_alph = {'A':0,'C':1,'G':2,'T':3,'N':4,'$':5,'a':0,'c':1,'g':2,'t':3,'n':4}
prime = 27162335252586509;

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('input', help='input file path', type=str)
	parser.add_argument('--check',  help='check for collisions (debug only)',action='store_true')
	args = parser.parse_args()

	# input file
	fname = args.input
	dic = {}
	collection = []
	no_seqs = 0
	int_intervals = 0
	int_inter_length = 0
	total_length = 0
	variability = 0
	max_len = 0
	suffixes = None

	print("Loading the input collection...")
	# scan the file and load collection
	with open(fname,'rb') as file:
		while True:
			header = file.readline().decode()
			if not header:
				break
			line = list(file.readline().decode())
			line[-1] = '$'
			collection.append(line)
			max_len = max(max_len,len(line))
		no_seqs = len(collection)
		#initialize vector marking sequences that can contain a left maximal suffix
		active = [1]*no_seqs
		not_active = 0
		hashes = [0]*no_seqs
		if args.check:
			suffixes = ['']*no_seqs
		#iterate through all suffixes
		i = 1
		start0 = time.time()
		print("Computing dataset properties...")
		while True:
			dic = {}
			for j in range(len(collection)):
				# proper suffixes
				if (len(collection[j])-i > 0) :
					total_length += 1
					if(active[j]==1):
						curr_hash = hashes[j] = ((hashes[j]*6)+DNA_alph[collection[j][len(collection[j])-i]])%prime
						if args.check:
							suffixes[j] = collection[j][len(collection[j])-i] + suffixes[j]
						# check if the hash suffix is in the dict
						if curr_hash in dic:
							dic[curr_hash][0] += 1
							dic[curr_hash][1][DNA_alph[collection[j][len(collection[j])-i-1]]] += 1 
							if args.check:
								if suffixes[j] != dic[curr_hash][3]:
									print("Error, collision occured, change the prime number, Exiting...")
									print(suffixes[j] +" vs "+dic[curr_hash][3])
									exit(1)
						else:
							freq = [0,0,0,0,0,0]
							freq[DNA_alph[collection[j][len(collection[j])-i-1]]] = 1
							if(args.check):
								dic[curr_hash] = [1,freq,j,suffixes[j]]
							else:
								dic[curr_hash] = [1,freq,j]
				# s_1$
				elif len(collection[j])-i == 0 :
					total_length += 1
					if(active[j]==1):
						curr_hash = hashes[j] = ((hashes[j]*6)+DNA_alph[collection[j][len(collection[j])-i]])%prime
						if args.check:
							suffixes[j] = collection[j][len(collection[j])-i] + suffixes[j]
						if curr_hash in dic:
							dic[curr_hash][0] += 1
							dic[curr_hash][1][5] += 1
							if args.check:
								if suffixes[j] != dic[curr_hash][3]:
									print("Error, collision occured, change the prime number, Exiting...")
									exit(1)
						else:
							if args.check:
								dic[curr_hash] = [1,[0,0,0,0,0,1],j,suffixes[j]]
							else:
								dic[curr_hash] = [1,[0,0,0,0,0,1],j]
		    # increment suffixes offset
			i += 1
			# scan all suffixes in the dictionary
			for key, value in dic.items():
				# if the interval is greater than 1
				if value[0] > 1:
					# if the interval is interesting
					if value[1].count(0) < 5: 
						int_intervals += 1
						int_inter_length += value[0]
						# remove 0 values from parick vector
						parick = [g for g in value[1] if g != 0]
						mind = parick.index(max(parick))
						li = list(range(len(parick)))
						li.remove(mind)
						sum_ot = 0
						# compute variability
						for x in li:
							sum_ot += parick[x]
						if parick[mind] <= (sum_ot + 1):
							variability += sum(parick)
						else:
							variability += (min(parick[mind],sum_ot)*2) + 1
				else:
					active[value[2]] = 0
					not_active += 1
			# if no other sequence pairs can have a left maximal shared suffix 
			if(not_active == no_seqs):
				for j in range(len(collection)):
					total_length += max(0,len(collection[j])-i)
				break
			# if we reached the end of the longest string stop
			if max_len-i == -1:
				break

		print("------ Data set properties: " + fname) 
		print("Data set properties ------ computation required: {0:.4f} sec".format(time.time()-start0))
		print("No. sequences: "+str(no_seqs))
		print("Number of interesting intervals: "+str(int_intervals))
		print("Total length: "+str(total_length))
		print("Total interesting intervals length: "+str(int_inter_length))
		print("Ratio interesting/total: "+str(int_inter_length/total_length))
		print("Maximum number of runs for interesting intervals: "+str(variability))
		print("Interesting intervals variability: "+str(variability/int_inter_length))

if __name__ == '__main__':
	main()