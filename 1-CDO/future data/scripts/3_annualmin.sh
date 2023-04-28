#!/bin/bash -l

# =============================================================================
# SUMMARY
# =============================================================================

# Code to take the annual minimum values for the future data

# =============================================================================
mkdir $WORKDIR/thesis/data/future_data/annualmin/
mkdir $WORKDIR/thesis/data/future_data/annualmin/ensemble_pairwiserealizations

indir=$WORKDIR/thesis/data/future_data/ensembles/
outdir=$WORKDIR/thesis/data/future_data/annualmin/ensemble_pairwiserealizations

#define filename components
models=("CanESM5" "CNRM-ESM2-1" "IPSL-CM6A-LR" "UKESM1-0-LL")
scenarios=("ssp126" "ssp370" "ssp126-ssp370Lu" "ssp370-ssp126Lu")

#==============================================================================
# get annual min TAS, annual average treeFrac, and annual max snd for all scenarios 
#==============================================================================
for scen in "${scenarios[@]}"; do
    echo ${scen}
    cd $indir/${scen}
    echo "tas"
    for FILE in tas*; do cdo yearmin $FILE ${outdir}/min_$FILE; done
    for FILE in tas*; do cdo yearmean $FILE ${outdir}/av_$FILE; done 
    echo "treeFrac"
    for FILE in treeFrac*; do cdo yearmean $FILE ${outdir}/min_$FILE; done
    echo "snd"
    for FILE in snd*; do cdo yearmax $FILE ${outdir}/min_$FILE; done
done
