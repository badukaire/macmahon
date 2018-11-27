#!/bin/sh

INPUT=test1
F_INPUT=${INPUT}.txt
DIR_IN=../testData

T01F=$DIR_IN/$F_INPUT

BYE="byeIgnore"
RNDS="r4_4"

OUTF_REGULAR=${INPUT}_sortRegular_${BYE}_${RNDS}.txt
OUTF_REG_SOS=${INPUT}_sortRegularSOS_${BYE}_${RNDS}.txt
OUTF_PT_WSOS=${INPUT}_sortWeightedSOS_${BYE}_${RNDS}.txt

REF_F_REGULAR=ref_${OUTF_REGULAR}
REF_F_REG_SOS=ref_${OUTF_REG_SOS}
REF_F_PT_WSOS=ref_${OUTF_PT_WSOS}

echo "generating -r 4 -b IGNORE -s REGULAR =>" $OUTF_REGULAR
python p.py -f $T01F -r 4 -d TABLE -b IGNORE -o $OUTF_REGULAR -s REGULAR
echo "comparing reference" ${REF_F_REGULAR} "with generated" ${OUTF_REGULAR}
diff -q ${REF_F_REGULAR} ${OUTF_REGULAR} || { echo "test FAILED" ; echo 1 ; }

echo "generating -r 4 -b IGNORE -s REGULARSOS =>" $OUTF_REG_SOS
python p.py -f $T01F -r 4 -d TABLE -b IGNORE -o $OUTF_REG_SOS -s REGULARSOS
echo "comparing reference" ${REF_F_REG_SOS} "with generated" ${OUTF_REG_SOS}
diff -q ${REF_F_REG_SOS} ${OUTF_REG_SOS} || { echo "test FAILED" ; echo 1 ; }

echo "generating -r 4 -b IGNORE -s WSOS =>" $OUTF_PT_WSOS
python p.py -f $T01F -r 4 -d TABLE -b IGNORE -o $OUTF_PT_WSOS -s WSOS
echo "comparing reference" ${REF_F_PT_WSOS} "with generated" ${OUTF_PT_WSOS}
diff -q ${REF_F_PT_WSOS} ${OUTF_PT_WSOS} || { echo "test FAILED" ; echo 1 ; }

