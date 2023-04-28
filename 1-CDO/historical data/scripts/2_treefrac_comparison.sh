#!/bin/bash -l

# =============================================================================
# SUMMARY
# =============================================================================

# Code to compare first time step of hist with hist-noLu for treefrac

# =============================================================================

#create folders
mkdir $WORKDIR/thesis/data/raw_copy/treeFrac/tstepfirst_hist
mkdir $WORKDIR/thesis/data/raw_copy/treeFrac/tsteplast_nolu
mkdir $WORKDIR/thesis/data/raw_copy/treeFrac/comparison

#define lists for iteration
models=("CNRM-ESM2-1" "IPSL-CM6A-LR" "UKESM1-0-LL")
realizations=("r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r1i1p1f2" "r2i1p1f2" "r3i1p1f2" "r4i1p1f2")


#select first time step
for mod in ${models[@]}; do
    echo $mod
    cd $WORKDIR/thesis/data/raw_copy/treeFrac/hist-noLu/$mod
    echo 'hist-noLU'
    for FILE in *; do
        #echo $FILE
        cdo seltimestep,1980 $FILE $WORKDIR/thesis/data/raw_copy/treeFrac/tsteplast_nolu/$FILE
    done
    cd $WORKDIR/thesis/data/raw_copy/treeFrac/historical/$mod
    echo 'historical'
    for FILE in *; do
        #echo $FILE
        cdo seltimestep,1 $FILE $WORKDIR/thesis/data/raw_copy/treeFrac/tstepfirst_hist/$FILE
    done
done


#compare 
for mod in ${models[@]}; do
    echo $mod
    for r in ${realizations[@]}; do
        cdo sub $WORKDIR/thesis/data/raw_copy/treeFrac/tstepfirst_hist/treeFrac_Lmon_${mod}_historical_${r}_*.nc $WORKDIR/thesis/data/raw_copy/treeFrac/tsteplast_nolu/treeFrac_Lmon_${mod}_hist-noLu_${r}_*.nc  $WORKDIR/thesis/data/raw_copy/treeFrac/comparison/treeFrac_Lmon_${mod}_comparison_${r}.nc
    done
done




