#!/bin/bash
# This script is to download information through multiprocess.
# Usage: ./download.sh conf.ini
# Author: Deng Fei

line=$(awk '/THREAD_NUM/{print $0}' $1);
threadNum=${line#THREAD_NUM=};
line=$(awk '/TEMP_PATH/{print $0}' $1);
path=${line#TEMP_PATH=};
line=$(awk '/DATA_TYPE/{print $0}' $1);
dataType=${line#DATA_TYPE=};
line=$(awk '/IDLIST_FILE/{print $0}' $1);
idlistFile=${line#IDLIST_FILE=};

echo "Thread number: $threadNum"
echo "Temp path: $path"

if [[ ! -d "$path" ]];then
	mkdir $path
fi
if [[ ! -d "$path/idlist" ]];then
	mkdir $path/idlist
fi

# Generata download list for every thread
idNum=$(wc -l $idlistFile | awk '{print $1}');
splitNum=$(($idNum/$threadNum + 1));
split -a 3 -l $splitNum $idlistFile -d $path/idlist/

for((i=0; i<$threadNum; i++))
do
	if (( $i >= 100 ));then
		idlist=$path/idlist/$i;
	elif (( $i >= 10 ));then
		idlist=$path/idlist/0$i;
	else
		idlist=$path/idlist/00$i;
	fi
	perl download.perl $1 < $idlist > $path/$i.txt 2>$path/$i.log &
done

echo "start waiting"

# Wait all the perl script finished
wait

echo "finish waiting"

# Get the missing information
if [[ -f "$path/missing.log" ]];then
	rm $path/missing.log
fi
awk '/bad/{print $0}' $path/*.log >> $path/missing.log
while [ 1 ]
do
	number=$(awk 'END{print NR}' $path/missing.log)
	if [[ "$number" < 10 ]];then
		break
	fi
	awk '/bad/{print $2}' $path/missing.log > $path/missing_idlist;
	perl download.perl $1 < $path/missing_idlist >> $path/missing.txt 2> $path/missing.log;
done

# Merge all the data into one big file
cat $path/*.txt >> ${dataType}_level0

exit 0
