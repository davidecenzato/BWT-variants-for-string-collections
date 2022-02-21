# Instructions for downloading the datasets used in the paper experiments

### Dependencies

- seqkit: https://github.com/shenwei356/seqkit
- sra-toolkit : https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit
- python3

#### For downloading all datasets but the SARSCov2genomes run the following command
```console
python DownloadData.py
```

All dataset will be place in the ./data subdirectory created by the script,
the SRA ids are
- SARSCov2short : SRR12038588
- SimonDivreads : ERR1019034 
- 16SrRNAshort  : SRR10391186
- InfluenzaA    : SRR10391186
- SARSCov2long  : downloaded at https://sra-pub-sars-cov2.s3.amazonaws.com/sra-src/SRR16287139/demultiplex.bc1021_BAK8B_OA--bc1021_BAK8B_OA.hifi_reads.fastq.gz.1
- 16rRNAlong:   : downloaded at https://drive5.com/opti_paper/supp_data.tar.gz
- CandidaAuris  : SRR7507278
- SARSCov2genomes: downloaded at https://www.covid19dataportal.org/ 

### Instructions for generating SARSCov2genomes dataset

Download the raw read from this link: https://www.covid19dataportal.org/sequences?db=embl-covid19&query=Severe%20acute%20respiratory%20syndrome%202&size=15&facets=creation_date:2019%2F01%2F01-2021%2F05%2F17&requestFrom=searchExample&crossReferencesOption=all#search-content

Filter the fasta selecting only the sequences with one of the headers in file "./data/SARSCov2genomes_ids.txt". Then,
replace each degenerate base in the sequences with a N. Take the first 50 sequences from the resulting fasta for the SARSCov2genomes_small dataset.

### Instructions for generating the other datasets manually

Download the datasets using either the SRA ids or the links, filter the sequences using the headers in "./data/filename_ids.txt". Then, select the first 5k and 1.5k sequences for the short and long sequence small datasets respectively.