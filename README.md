# Description

Many studies analyze issue tracking repositories to understand and support software
development.
To facilitate the analyses, we share a Mozilla issue tracking dataset covering
a 15-year history.
The dataset includes three extracts and multiple levels for each extract.
The three extracts were retrieved through two channels, a front-end (web user interface (UI)),
and a back-end (official database dump) of Mozilla Bugzilla at three different times.
The variations (dynamics) among extracts provide space
for researchers to reproduce and validate their studies,
while revealing potential opportunities for studies that otherwise could not be conducted.
We provide different data levels for each extract
ranging from raw data to standardized data as well as to the calculated data level for targeting 
specific research questions.
Data retrieving and processing scripts related to each data level are offered too.
By employing the multi-level structure, analysts can more efficiently start an inquiry from the
standardized level and easily trace the data chain when necessary (e.g., to verify if a phenomenon 
reflected by the data is an actual event).
We applied this dataset to several published studies and intend
to expand the multi-level and multi-extract feature to other software engineering 
datasets.

# Notes
We recommend `Download ZIP` function instead of repository clone for downloading the dataset.
If you have difficulties to download the big zip package, please download file by file with specified path,
e.g., `https://raw.githubusercontent.com/jxshin/mzdata/master/data/2011/level0/activity/activity_level0.gz_aa`.

The data files are compressed and split into multiple subfiles, please use `cat` to merge and
use `gzip` to uncompress.
For example:
```
$ cat data/2011/level1/information/info_level1.gz_* > info_level1.gz
$ gzip -d info_level1.gz
``` 
