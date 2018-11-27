#!/bin/sh

INPUT=test1
F_INPUT=${INPUT}.txt
DIR_IN=../testData
T01F=$DIR_IN/$F_INPUT

PYSCRIPT=../src/macmahon.py

BYE="byeIgnore"
RNDS="r4_4"

OUTF_REGULAR=${INPUT}_sortRegular_${BYE}_${RNDS}.txt
OUTF_REG_SOS=${INPUT}_sortRegularSOS_${BYE}_${RNDS}.txt
OUTF_PT_WSOS=${INPUT}_sortWeightedSOS_${BYE}_${RNDS}.txt

REF_F_REGULAR=ref_${OUTF_REGULAR}
REF_F_REG_SOS=ref_${OUTF_REG_SOS}
REF_F_PT_WSOS=ref_${OUTF_PT_WSOS}

echo OUTF_REGULAR $OUTF_REGULAR
echo OUTF_REG_SOS $OUTF_REG_SOS
echo OUTF_PT_WSOS $OUTF_PT_WSOS

echo "REF with -O : test1_sortRegular_byeIgnore_r4_4.txt"
echo "cmp with -o : $OUTF_REGULAR"

echo REF_F_REGULAR $REF_F_REGULAR
echo REF_F_REG_SOS $REF_F_REG_SOS
echo REF_F_PT_WSOS $REF_F_PT_WSOS

echo "REF with -O : test1_sortRegular_byeIgnore_r4_4.txt"
echo "cmp test: $REF_F_REGULAR"


echo "generating -r 4 -b IGNORE -s REGULAR =>" $OUTF_REGULAR
python $PYSCRIPT -f $T01F -r 4 -d TABLE -b IGNORE -o $OUTF_REGULAR -s REGULAR >/dev/null
echo "comparing reference" ${REF_F_REGULAR} "with generated" ${OUTF_REGULAR}
diff -q ${REF_F_REGULAR} ${OUTF_REGULAR} || { echo "test FAILED" ; echo 1 ; }
echo "[test OK]"
rm ${OUTF_REGULAR}


echo "generating -r 4 -b IGNORE -s REGULARSOS =>" $OUTF_REG_SOS
python $PYSCRIPT -f $T01F -r 4 -d TABLE -b IGNORE -o $OUTF_REG_SOS -s REGULARSOS >/dev/null
echo "comparing reference" ${REF_F_REG_SOS} "with generated" ${OUTF_REG_SOS}
diff -q ${REF_F_REG_SOS} ${OUTF_REG_SOS} || { echo "test FAILED" ; echo 1 ; }
echo "[test OK]"
rm ${OUTF_REG_SOS}

echo "generating -r 4 -b IGNORE -s WSOS =>" $OUTF_PT_WSOS
python $PYSCRIPT -f $T01F -r 4 -d TABLE -b IGNORE -o $OUTF_PT_WSOS -s WSOS >/dev/null
echo "comparing reference" ${REF_F_PT_WSOS} "with generated" ${OUTF_PT_WSOS}
diff -q ${REF_F_PT_WSOS} ${OUTF_PT_WSOS} || { echo "test FAILED" ; echo 1 ; }
echo "[test OK]"
rm ${OUTF_PT_WSOS}

