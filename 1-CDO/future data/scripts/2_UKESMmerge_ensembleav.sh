#!/bin/bash -l

# =============================================================================
# SUMMARY
# =============================================================================

# Code to merge the UKESM files into one future period and take the pairwise ensemble averages and multimodel average

# =============================================================================

#define lists for iteration
scenarios=("ssp126" "ssp370" "ssp126-ssp370Lu" "ssp370-ssp126Lu")
variables=("tas" "treeFrac" "snd")
realizations=("r1i1p1f2" "r2i1p1f2" "r3i1p1f2" "r4i1p1f2" "r8i1p1f2")
: '
#do time merge 
echo "time merge UKESM"
for scen in "${scenarios[@]}"; do
    echo ${scen}
    cd $WORKDIR/thesis/data/future_data/${scen}
    for var in "${variables[@]}"; do
        echo ${var}
        for r in "${realizations[@]}"; do
            cdo mergetime ${var}_*_UKESM1-0-LL_${scen}_${r}_gn_201501-204912.nc ${var}_*_UKESM1-0-LL_${scen}_${r}_gn_205001-210012.nc ${var}_UKESM1-0-LL_${scen}_${r}_gn_201501-210012.nc
        done
    done        
done

#create folders for ensemble data
echo "creating ensemble folders"
mkdir $WORKDIR/thesis/data/future_data/ensembles
for scen in "${scenarios[@]}"; do
    echo ${scen}
    mkdir $WORKDIR/thesis/data/future_data/ensembles/${scen}
done
'
indir=$WORKDIR/thesis/data/future_data
outdir=$WORKDIR/thesis/data/future_data/ensembles



#then get ensemble mean for each scenario and each variable (just copy the CanESM5 and CNRM files as there is only one realization)
echo "taking ensemble averages"
for scen in "${scenarios[@]}"; do
    echo ${scen}
    for var in "${variables[@]}"; do
        echo ${var}
        :'
        cdo ensmean  $indir/${scen}/${var}_UKESM1-0-LL_${scen}_*_gn_201501-210012.nc $outdir/${scen}/${var}_UKESM1-0-LL_${scen}_ensembleav_gn_201501-210012.nc
        echo "copy CanESM5"
        cp $indir/${scen}/${var}_*_CanESM5_${scen}_*.nc $outdir/${scen}/
        echo "copy CNRM-ESM2-1"
        cp $indir/${scen}/${var}_*_CNRM-ESM2-1_${scen}_*.nc $outdir/${scen}/
        '
        echo "copy IPSL-CM6A-LR"
        cp $indir/${scen}/${var}_*_IPSL-CM6A-LR_${scen}_*.nc $outdir/${scen}/
    done
done

#regrid data to prepare for multimodel averaging 
for scen in "${scenarios[@]}"; do
    echo ${scen}
    cd $outdir/${scen}
    for file in *; do
        cdo remapbil,treeFrac_Lmon_CanESM5_${scen}_r1i1p2f1_gn_201501-210012.nc $file regrid_$file
    done
done

#take multimodel average and remove regrid clutter
echo "taking multimodel averages"
for scen in "${scenarios[@]}"; do
    echo ${scen}
    for var in "${variables[@]}"; do
        echo ${var}
        cdo ensmean  $outdir/${scen}/regrid_${var}_*_${scen}_*.nc $outdir/${scen}/${var}_${scen}_multimodelav.nc
    done
done

for scen in "${scenarios[@]}"; do
    echo ${scen}
    cd $outdir/${scen}
    rm regrid_*
done
