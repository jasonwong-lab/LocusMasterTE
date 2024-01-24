## Paper
https://www.biorxiv.org/content/10.1101/2023.03.21.533716v1

## Installation
Before creating conda environment, please ensure packages are installed.


```
conda create -n LocusMasterTE python=3.6 future pyyaml cython=0.29.7 numpy=1.16.3 pandas=1.1.3 scipy=1.2.1 intervaltree=3.0.2

conda activate LocusMasterTE 
conda install -c bioconda htslib
pip install pysam==0.15.2
git clone https://github.com/jasonwong-lab/LocusMasterTE.git
cd LocusMasterTE
python3 setup.py build | python3 setup.py install 
LocusMasterTE bulk assign -h
```
## Preprocessing Wrapper
LocusMasterTE provides a preprocessing wrapper script from Long-Read FASTQs to LocusMasterTE input. \
First, tools need to be installed. You may refer website for installation. \
* Pychopper : https://github.com/epi2me-labs/pychopper
* Minimap : https://github.com/lh3/minimap2
* Samtools : https://www.htslib.org/
* FeatureCounts : https://rnnh.github.io/bioinfo-notebook/docs/featureCounts.html
  \
4 inputs are needed.
```
1. Genomic FASTA
2. Long Read FASTQ
3. Gene and TE GTF files
4. Path to Output Directory
```
Example code is below. 
```bash LocusMasterTE/long_read_wrapper.sh hg38.fasta long_read.fastq.gz hg38.gtf output_path```

If you have short-read FASTQ, here is the recommended code.
```
STAR --runThreadN 20 --genomeDir $outdir/STAR_index \
   --readFilesIn $short_fq1 $short_fq2 --readFilesCommand zcat --outFileNamePrefix STAR_output \
   --outSAMtype BAM Unsorted --outSAMstrandField intronMotif --outSAMattributes All --outSAMattrIHstart 0 \
   --outFilterMultimapNmax 100 --outFilterScoreMinOverLread 0.4 --outFilterMatchNminOverLread 0.4 --clip3pNbases 0 \
   --winAnchorMultimapNmax 100 --alignEndsType EndToEnd --alignEndsProtrude 100 DiscordantPair --chimSegmentMin 250 --twopassMode Basic
# sort by read name
samtools collate -o Aligned_sort_name.out.bam --output-fmt BAM Aligned_sort.out.bam
```

If you have short-read BAM file, BAM file needs to be sorted by read name. 
Run command below. And output bam can be readily input in LocusMasterTE. \
```samtools collate -o Aligned_sort_name.out.bam --output-fmt BAM Aligned_sort.out.bam```

## Testing
```bash LocusMasterTE/data/run_sample.sh```

A BAM file (`sample_alignment_sort.bam`), annotation (`annotation.gtf`) and long read TPM file (`long_read_data.txt`) are included in
LocusMasterTE/data folder. \
Recommended command line is written in bash file (`run_sample.sh`).

## BAM file
When inputting BAM file, it should be sorted by READ NAME. Otherwise, LocusMasterTE does not work properly.<br />
Aligned by coordinate also is not applicable. 

## Usage
* [`LocusMasterTE bulk assign`]

LocusMasterTE was built upon Telescope. Additional arguments are elaborated.

### LocusMasterTE exclusive options:

```
  long_read
                        Mandatory argument. 
                        Path to long read file composed of three columns: "Geneid", "TPM", and "subF". 
                        "Geneid" represents TE individual names followed by TPM values in "TPM" coulmn. 
                        Belonging subfamily information from RepeatMasker database goes under "subF".
                        (default: None)
  Run Modes:

  --reassign_mode {exclude,choose,average,conf,unique,long_read}
                        Reassignment mode. After EM is complete, each fragment
                        is reassigned according to the expected value of its
                        membership weights. The reassignment method is the
                        method for resolving the "best" reassignment for
                        fragments that have multiple possible reassignments.
                        Available modes are: "exclude" - fragments with
                        multiple best assignments are excluded from the final
                        counts; "choose" - the best assignment is randomly
                        chosen from among the set of best assignments;
                        "average" - the fragment is divided evenly among the
                        best assignments; "conf" - only assignments that
                        exceed a certain threshold (see --conf_prob) are
                        accepted; "unique" - only uniquely aligned reads are
                        included. "long_read" - use long read to determine best hit.
                        NOTE: Results using all assignment modes are
                        included in the LocusMasterTE report by default. This
                        argument determines what mode will be used for the
                        "final counts" column. (default: exclude)

Model Parameters:

  --rescue_short RESCUE_SHORT
                        To rescue features only captured by short, 
                        values can be given to 0 expression captured in long read.
                        (default: 0)
  --long_read_weight {float}
                        Weights on long-read information; No limited numeric ranges.
                        Higher number is recommended when matched tissue or cell type long-read is inputted.
                        Lower number is recommended when using different tissue samples.
                        (default: 1)
  --prior_change {all,theta,none}
                        Integration of TPM counts from long reads. 
                        All represents change in both pi and theta.
                        Change in theta influences only multimapping counts.
                        None is equivalent to not integrating long read
                        (default: all)
```

### Arguments from Telescope
<details>
<summary>From Telescope</summary>

```
  samfile               Path to alignment file. Alignment file can be in SAM
                        or BAM format. File must be collated so that all
                        alignments for a read pair appear sequentially in the
                        file.
  gtffile               Path to annotation file (GTF format)
  --attribute ATTRIBUTE
                        GTF attribute that defines a transposable element
                        locus. GTF features that share the same value for
                        --attribute will be considered as part of the same
                        locus. (default: locus)
  --no_feature_key NO_FEATURE_KEY
                        Used internally to represent alignments. Must be
                        different from all other feature names. (default:
                        __no_feature)
  --tempdir TEMPDIR     Path to temporary directory. Temporary files will be
                        stored here. Default uses python tempfile package to
                        create the temporary directory. (default: None)

Reporting Options:

  --quiet               Silence (most) output. (default: False)
  --debug               Print debug messages. (default: False)
  --logfile LOGFILE     Log output to this file. (default: None)
  --outdir OUTDIR       Output directory. (default: .)
  --exp_tag EXP_TAG     Experiment tag (default: telescope)
  --updated_sam         Generate an updated alignment file. (default: False)
  
  Run Modes:
  --conf_prob CONF_PROB
                        Minimum probability for high confidence assignment.
                        (default: 0.9)
  --overlap_mode {threshold,intersection-strict,union}
                        Overlap mode. The method used to determine whether a
                        fragment overlaps feature. (default: threshold)
  --overlap_threshold OVERLAP_THRESHOLD
                        Fraction of fragment that must be contained within a
                        feature to be assigned to that locus. Ignored if
                        --overlap_method is not "threshold". (default: 0.2)
  --annotation_class {intervaltree,htseq}
                        Annotation class to use for finding overlaps. Both
                        htseq and intervaltree appear to yield identical
                        results. Performance differences are TBD. (default:
                        intervaltree)                    
  --stranded_mode {None, RF, R, FR, F}
                        Options for considering feature strand when assigning reads. 
                        If None, for each feature in the annotation, returns counts 
                        for the positive strand and negative strand. If not None, 
                        this argument specifies the orientation of paired end reads 
                        (RF - read 1 reverse strand, read 2 forward strand) and
                        single end reads (F - forward strand) with respect to the 
                        generating transcript. (default: None)
Model Parameters:

  --pi_prior PI_PRIOR   Prior on π. Equivalent to adding n unique reads.
                        (default: 0)
  --theta_prior THETA_PRIOR
                        Prior on θ. Equivalent to adding n non-unique reads.
                        (default: 200000)
  --em_epsilon EM_EPSILON
                        EM Algorithm Epsilon cutoff (default: 1e-7)
  --max_iter MAX_ITER   EM Algorithm maximum iterations (default: 100)
  --use_likelihood      Use difference in log-likelihood as convergence
                        criteria. (default: False)
  --skip_em             Exits after loading alignment and saving checkpoint
                        file. (default: False)
```       
</details>

## Output

LocusMasterTE has three main output files: the transcript counts estimated via EM (`LocusMasterTE-TE_counts.tsv`).\
The count file is most important for downstream analysis.
