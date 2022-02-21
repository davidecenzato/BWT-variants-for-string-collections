# Instructions for computing all BWT variants used in paper experiments

### Dependencies

- [Big-BWT](https://github.com/alshai/Big-BWT.git) 
- [PFP-eBWT](https://github.com/davidecenzato/PFP-eBWT.git)
- [ropebwt2](https://github.com/lh3/ropebwt2.git)
- [SeqKit](https://github.com/shenwei356/seqkit.git)

### Compilation

Compile Big-BWT and PFP-eBWT tools as usual (more information at the links given above). For compiling ropebwt2 substitute the main in "./ropebwt2" with the "main.c" in the "./ropebwt2main" subdirectory, then compile. 

### Run

Use the following command for computing all BWT variants,
```console
python compute_all_bwt_variants.py --all
```

All BWT variants will be place in the "./BWTvar" subdirectory