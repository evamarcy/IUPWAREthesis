#!/bin/bash -l

# =============================================================================
# SUMMARY
# =============================================================================

# Code to reduce treeFrac and TAS files to annual values
# calculates gridarea for each model
# Calculates two annual values: winter average AND annual minimum monthly TAS Max

# =============================================================================
# INITIALIZATION
# =============================================================================

# set input directory
inDIR=$WORKDIR/thesis/data/raw_copy

# set output directories
minoutDIR=$WORKDIR/thesis/data/annualmin/individual_pairwiserealizations
ensminoutDIR=$WORKDIR/thesis/data/annualmin/ensemble_pairwiserealizations


#define filename components
models=("CanESM5" "CNRM-ESM2-1" "IPSL-CM6A-LR" "UKESM1-0-LL")
scenarios=("hist-noLu" "historical")


#==============================================================================
# get TAS for both historical and hist-noLu, winter average and minimum annual 
echo "processing TAS files"
#==============================================================================
for scen in "${scenarios[@]}"; do
    echo ${scen}
    for mod in "${models[@]}"; do
        echo ${mod}
        cd $inDIR/tas/${scen}/${mod}
        echo "taking annual mean"
        for FILE in *; do cdo yearmean $FILE ${minoutDIR}/av_$FILE; done 
    done
done


# =============================================================================
# ensemble average with pairwise realizations only
echo "taking ensemble averages"
# =============================================================================

for scen in "${scenarios[@]}"; do
    echo ${scen}
    for mod in "${models[@]}"; do
        echo ${mod}
        cdo ensmean ${minoutDIR}/av_tas_*_${mod}_${scen}_*.nc ${ensminoutDIR}/av_ensembleav_tas_${scen}_${mod}.nc
    done
done


# =============================================================================
# regrid the ensemble averages to match all the same grid and take multimodel average before removing regrid files
echo "taking multimodel averages"
# =============================================================================

cd ${ensminoutDIR}
for file in av_ensembleav_tas*; do
    cdo remapbil,min_ensembleav_treeFrac_historical_CanESM5.nc $file regrid_$file
done


for scen in "${scenarios[@]}"; do
    echo ${scen}
    cdo ensmean regrid_av_ensembleav_tas_${scen}_*.nc av_multimodelav_${var}_${scen}.nc
done

rm regrid*