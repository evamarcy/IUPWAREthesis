#!/bin/bash -l

# =============================================================================
# SUMMARY
# =============================================================================

# Code to copy files from CMIP6 folder to working directory

# =============================================================================


#define lists for iteration
scenarios=("ssp126" "ssp370")
models=("CanESM5" "CNRM-ESM2-1" "IPSL-CM6A-LR" "UKESM1-0-LL")
variables=("tas" "treeFrac" "snd")


#create folders
for scen in "${scenarios[@]}"; do
    mkdir $WORKDIR/thesis/data/future_data/${scen}
done


for scen in "${scenarios[@]}"; do
    echo $scen
    for var in "${variables[@]}"; do
: '
        mod="CanESM5"
        group="CCCma"
        realizations=("r1i1p2f1")
        for r in "${realizations[@]}"; do
            cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/ScenarioMIP/${group}/${mod}/${scen}/${r}/*/${var}/*/*/${var}_*_${mod}_${scen}_${r}_*.nc $WORKDIR/thesis/data/future_data/${scen}/
        done

        mod="CNRM-ESM2-1"
        group="CNRM-CERFACS"
        realizations=("r1i1p1f2")
        for r in "${realizations[@]}"; do
            cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/ScenarioMIP/${group}/${mod}/${scen}/${r}/*/${var}/*/*/${var}_*_${mod}_${scen}_${r}_*.nc $WORKDIR/thesis/data/future_data/${scen}/
        done

        mod="UKESM1-0-LL"
        group="MOHC"
        realizations=("r1i1p1f2" "r2i1p1f2" "r3i1p1f2" "r4i1p1f2" "r8i1p1f2")
        for r in "${realizations[@]}"; do
            cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/ScenarioMIP/${group}/${mod}/${scen}/${r}/*/${var}/*/*/${var}_*_${mod}_${scen}_${r}_*.nc $WORKDIR/thesis/data/future_data/${scen}/
        done
'
        mod="IPSL-CM6A-LR"
        group="IPSL"
        realizations=("r1i1p1f1")
        for r in "${realizations[@]}"; do
            cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/ScenarioMIP/${group}/${mod}/${scen}/${r}/*/${var}/*/*/${var}_*_${mod}_${scen}_${r}_*.nc $WORKDIR/thesis/data/future_data/${scen}/
        done


    done
done