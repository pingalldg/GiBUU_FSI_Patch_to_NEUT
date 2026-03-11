#!/bin/bash

# Create 100 folders named folder1 to folder100
for i in {50001..80000}
do
cd $i
rm -rf  PYR.RG Multiplicity_* GiBUU_database* NucleonVacuumMass.dat sigma.dat sigma.dat neutrino_info.dat main.run ReAdjust.PlotPot.* DensTab_target.dat
rm -rf qsub spool
rm -rf GiBUU.x 

cd ..
done
