# vcfkit
Tools &amp; scripts I use to process our VCFs. 

`**vcf_stats**`
Generate PDF with useful statistics concerning VCF tags

Choose from boxplot, cumulative distribution, piechart plottypes depending on
variable data type
Generate PDF report
    
Usage:
vcf_stats.py [-h] [-c PLOT_CONFIG_FILE] [-t TAGS] [-v] in_vcf pdf_path

positional arguments:
  in_vcf                Input VCF file
  pdf_path              Write PDF report to this path

optional arguments:
  -h, --help            show this help message and exit
  -c PLOT_CONFIG_FILE, --plot_config_file PLOT_CONFIG_FILE
                        YAML file with info for plotting (labels, scale, ...)
  -t TAGS, --tags TAGS  VCF Format, Filter or Info tags to be analyzed
  -v, --version         show program's version number and exit