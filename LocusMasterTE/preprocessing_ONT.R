#!/usr/bin/env Rscript
#install.packages("tidyverse")
#install.packages("optparse")

library("optparse")
library("tidyverse")
option_list = list(
  make_option(c("-f", "--file"), type="character", default=NULL, 
              help="featureCounts file", metavar="character"),
  make_option(c("-o", "--out"), type="character", default="long_read_subF_TPM.txt", 
              help="output long read TPM file [default= %default]", metavar="character")
); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

if (is.null(opt$file)){
  print_help(opt_parser)
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
}

fc_out <- read.delim(opt$file, comment.char="#")
tpm3 <- function(counts,len) {
  x <- counts/len
  return(t(t(x)*1e6/sum(x)))
}

fc_out$tpm <- tpm3(fc_out[,7], fc_out$Length)
fc_out <- fc_out[!str_detect(fc_out[,1], "ENSG"),c(1,8)]
fc_out$subF <- unlist(sapply(strsplit(fc_out[,1], "_", fixed=TRUE), function(x) x[1], simplify=FALSE))
colnames(fc_out) <- c("Geneid","TPM","subF")
write.table(fc_out, file=opt$out, row.names=FALSE, col.names=TRUE, sep="\t", quote=FALSE)







