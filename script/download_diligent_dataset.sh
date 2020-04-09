#!/bin/bash
# sh download_diligent_dataset.sh /mnt

URL="https://www.dropbox.com/s/hdnbh526tyvv68i/DiLiGenT.zip?dl=0"
NAME="DiLiGenT"

DATASET_DIR=${1%/}/$NAME
TMP_FILE=${1%/}/${NAME}.zip

if [ -e ${DATASET_DIR} ]; then
    echo "Already downloaded"
    exit 1
fi

wget $URL -O $TMP_FILE
unzip $TMP_FILE -d ${1%/}
rm $TMP_FILE