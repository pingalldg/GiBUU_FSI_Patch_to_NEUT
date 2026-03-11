#!/bin/bash

mcdir="/path_to_workdir/"
tagbase="job"
jobbase="GiBUU"
binary="/path_to_release/release/testRun/GiBUU.x"  # Define the path to the binary just once

# Number of directories/runs
for run in {6..7}; do
    OUTDIR="${mcdir}/${run}/"
    mkdir -p "$OUTDIR/qsub" "$OUTDIR/spool"

    cd "${OUTDIR}/qsub" || exit 1

    nrun=1  # Number of jobs per folder; you can adjust this

    for i in $(seq 1 $nrun); do
        parallelID=""  # Customize if you have multiple parallel jobs
        tag="$(printf "${tagbase}${parallelID}%d" "$i")"
        script="${OUTDIR}/spool/${tag}.pbs"

        if [ ! -f "${script}" ]; then
            cat <<EOF > "${script}"
#!/bin/bash
cd "${mcdir}/${run}" || exit 1
# Run the binary directly without copying it
${binary} < 005_Neutrino_T2K-numu.job > jg.log
cd "${OUTDIR}"
EOF
            chmod +x "${script}"
        else
            echo "${script} already exists"
            exit 57
        fi
    done

    # Submit job array
    outbase="${OUTDIR}/qsub/${tagbase}${parallelID}%I"
    bsub -q s \
         -J "${jobbase}${parallelID}[1-${nrun}]" \
         -e "${outbase}.e" \
         -o "${outbase}.o" \
         "${OUTDIR}/spool/${tagbase}${parallelID}\$LSB_JOBINDEX.pbs"

    echo "Submitted jobs for run ${run}. Check status with \`bjobs\` or \`qstat\`."
done
