#!/bin/bash
#BSUB -q s
#BSUB -J tfb[51-80]
#BSUB -o logs/tfb_%I.out
#BSUB -e logs/tfb_%I.err

cd /path_to_workdir/
. ../setup.sh

# Calculate start and end indices for this array job
batch_size=1000
start=$(( ($LSB_JOBINDEX - 1) * batch_size + 1 ))
end=$(( $LSB_JOBINDEX * batch_size ))

echo "Processing batch $LSB_JOBINDEX: $start to $end"

./mkdir.sh $start $end
