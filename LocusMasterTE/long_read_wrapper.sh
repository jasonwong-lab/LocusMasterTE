hg38_fa=$1
long_fq=$2
GTF=$3
outdir=$4

### Processing Long-read ###
echo "Start Long-Read Processing..."

## pychopper
echo "Step 1: Run Pychopper"
pychopper ${long_fq}_pychopper.fastq.gz $long_fq

# Minimap2
echo "Step 2: Run Minimap"

minimap2 -ax splice $hg38_fa ${long_fq}_pychopper.fastq.gz > $outdir/${name}_processed.sam
samtools view -bS $outdir/${name}_processed.sam > $outdir/${name}_processed.bam
rm $outdir/${name}_processed.sam

# featureCounts
echo "Step 3: Run FeatureCounts"

featureCounts -T 5 -O -L -M -o $outdir/${name}_fc_output -a $GTF ${name}_processed.bam

# convert output
echo "Step 4: Convert to TPM"

Rscript --vanilla LocusMasterTE/preprocessing_ONT.R --file=${name}_processed.bam --out=${name}_long_read_subF_TPM.txt

echo "Finish Pre-processing Long-Read"
