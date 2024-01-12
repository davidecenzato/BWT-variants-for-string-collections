# BWT-variants-for-string-collections
This repository contains all scripts to reproduce the experiments showed in the paper "A theoretical and experimental analysis of BWT variants for string collections" presented at CPM 2022.

# Usage

### Download and Compile

```console
git clone https://github.com/davidecenzato/BWT-variants-for-string-collections.git
git submodule update --init --recursive
git submodule update --init --remote ropebwt2
```
Compile the 3 tools, Big-BWT, PFP-eBWT and ropeBWT2 downloaded as submodules. See ./BWTvar/compute_BWTs_instructions.md for the full instructions.
```console
cd bigbwt
make

cd pfpebwt
mkdir build
cd build
cmake ..
make

cp ropeBWT2main/main.c ./ropebwt2/
cd ropebwt2
make
```
Install SRA-toolkit, SeqKit tools and Levenshtein python package. See also ./data/download_instructions.md. 

### Datasets setup:

Most of the data can be downloaded using the following command,
```console
python3 DownloadData.py
```
The complete download instructions, including all dependencies, can be found in ./data/download_instruction.md. All datasets
will be stored in ./data subdirectory.

### BWT variants computation:

All BWT variants can be computed using the following command,
```console
python3 compute_all_bwt_variants.py --all
```
The complete instructions for computing the BWT variants, including all dependencies, can be found in ./BWTvar/compute_BWTs_instruction.md. All BWT variants will be stored in ./BWTvar subdirectory.

### Computation of Hamming distance, edit distance and number of runs:

All distances and number of runs can be computed using the following command,

```console
python3 compute_all_dist_runs.py --all
```
Computing the edit distance on long sequence datasets can take long time (> 24h), in case you can avoid computing the edit distance on those datasets use the following command,

```console
python3 compute_all_dist_runs.py --all --noeditlong
```
All results will be stored in ./results subdirectory.

### Computation of the dataset properties:

The properties of all datasets can be computed usign the following command,
```console
python3 -u compute_all_dataset_properties.py --all 
```
All results will be stored in ./results/dataset_properties.txt

# External resources

* [Big-BWT](https://github.com/alshai/Big-BWT.git)
* [gSACA-K](https://github.com/felipelouza/gsa-is.git)
* [malloc_count](https://github.com/bingmann/malloc_count.git)
* [PFP-eBWT](https://github.com/davidecenzato/PFP-eBWT.git)
* [ropeBWT2](https://github.com/lh3/ropebwt2.git)
* [sdsl-lite](https://github.com/simongog/sdsl-lite.git)
* [SeqKit](https://github.com/shenwei356/seqkit.git)

# Authors

### Theoretical results:

* Davide Cenzato
* Zsuzsanna Lipták

### Implementation and experiments:

* [Davide Cenzato](https://github.com/davidecenzato) 

# References and citations

[1] Davide Cenzato, Zsuzsanna Lipták: A Theoretical and Experimental Analysis of BWT Variants for String Collections. CPM 2022: 25:1-25:18 ([go to the paper](https://doi.org/10.4230/LIPIcs.CPM.2022.25))

[2] Davide Cenzato, Zsuzsanna Lipták: A survey of BWT variants for string collections. CoRR abs/2202.13235 (2022) ([go to the paper](https://arxiv.org/abs/2202.13235))

Please, if you use this work in an academic setting cite the following papers:

### conference version
    @inproceedings{CenzatoL22,
      author       = {Davide Cenzato and
                      Zsuzsanna Lipt{\'{a}}k},
      title        = {A Theoretical and Experimental Analysis of {BWT} Variants for String Collections},
      booktitle    = {Proc. of 33rd Annual Symposium on Combinatorial Pattern Matching, {CPM} 2022},
      series       = {LIPIcs},
      volume       = {223},
      pages        = {25:1--25:18},
      year         = {2022},
      doi          = {10.4230/LIPICS.CPM.2022.25}}
    

### extended version
    @article{CenzatoL22ext,
      author       = {Davide Cenzato and
                      Zsuzsanna Lipt{\'{a}}k},
      title        = {A survey of BWT variants for string collections},
      journal      = {CoRR},
      volume       = {abs/2202.13235},
      year         = {2022}}
