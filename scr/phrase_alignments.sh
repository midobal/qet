#!/bin/bash

if [ $# -ne 3 ];then
    >&2 echo "Usage: HMMAlignment.sh <src_file> <trg_file.es> <mgiza_path>"
    exit 0
fi

prefix=/tmp/qet

mkdir -p $prefix
text_1=$1 
text_2=$2

name_1=`basename ${text_1}`
name_2=`basename ${text_2}`

mgiza=$3


${mgiza}/plain2snt ${text_1} ${text_2} -snt1  ${prefix}/${name_1}_${name_2}.snt -snt2  ${prefix}/${name_2}_${name_1}.snt -vcb1  ${prefix}/${name_1}.vcb -vcb2  ${prefix}/${name_2}.vcb > /dev/null 2> /dev/null

${mgiza}/snt2cooc ${prefix}/${name_1}_${name_2}.cooc  ${prefix}/${name_1}.vcb  ${prefix}/${name_2}.vcb  ${prefix}/${name_1}_${name_2}.snt > /dev/null 2> /dev/null

${mgiza}/mgiza -s ${prefix}/${name_1}.vcb -t  ${prefix}/${name_2}.vcb -c  ${prefix}/${name_1}_${name_2}.snt -coocurrencefile  ${prefix}/${name_1}_${name_2}.cooc -o ${prefix}/${name_1}_${name_2} -hmmdumpfrequency 1 > /dev/null 2> /dev/null

cat ${prefix}/${name_1}_${name_2}.A3.final.part00* | awk '{if ($1 == "NULL" || $1 == "#") print $0}' | sed ':a;N;$!ba;s/\n/ /g' | sed 's/# Sentence/\n # Sentence/g' | sed '/^$/d' | sed 's/(//g' | sed 's/)//g' | sort -n -k 4 | awk -F "NULL" '{print $2}' | sed 's/[^0-9 {}]*//g' | sed 's/}[ |0-9]*{/ | /g' | sed 's/  /|/g' | sed 's/|[| ]*/ | /g' | sed 's/{//g' | sed 's/}//g' > ${prefix}/phrases
