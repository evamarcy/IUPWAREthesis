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

# create and set output directories
mkdir $WORKDIR/thesis/data/gridarea
mkdir $WORKDIR/thesis/data/annualmin
mkdir $WORKDIR/thesis/data/winteraverage
mkdir $WORKDIR/thesis/data/annualmin/individual_pairwiserealizations
mkdir $WORKDIR/thesis/data/winteraverage/individual_pairwiserealizations

gridDIR=$WORKDIR/thesis/data/gridarea
minoutDIR=$WORKDIR/thesis/data/annualmin/individual_pairwiserealizations
avoutDIR=$WORKDIR/thesis/data/winteraverage/individual_pairwiserealizations

#define filename components
models=("CanESM5" "CNRM-ESM2-1" "IPSL-CM6A-LR" "UKESM1-0-LL")
scenarios=("hist-noLu" "historical")
realization1=("r1i1p1f1" "r1i1p1f2" "r1i1p1f1" "r1i1p1f2")


#==============================================================================
# get gridsize for each model
echo "processing gridsize"
#==============================================================================
for i in "${!models[@]}"; do  
    cdo gridarea ${inDIR}/tas/historical/${models[$i]}/tas_Amon_${models[$i]}_historical_${realization1[$i]}_g*.nc ${gridDIR}/gridarea_${models[$i]}.nc
done

#==============================================================================
# get TAS for both historical and hist-noLu, winter average and minimum annual 
echo "processing TAS files"
#==============================================================================
for scen in "${scenarios[@]}"; do
    echo ${scen}
    for mod in "${models[@]}"; do
        echo ${mod}
        cd $inDIR/tas/${scen}/${mod}
        echo "taking annual min"
        for FILE in *; do cdo yearmin $FILE ${minoutDIR}/min_$FILE; done 
        echo "taking seasonal average"
        #winter in asia, europe, north america
        for FILE in *; do cdo -L selseas,DJF -seasmean  $FILE  ${avoutDIR}/DJF_$FILE; done
        #winter in south america, most of africa, australia
        for FILE in *; do cdo -L selseas,JJA -seasmean  $FILE  ${avoutDIR}/JJA_$FILE; done
    done
done

#==============================================================================
# get TASmax for both historical and hist-noLu, winter average and minimum annual 
echo "processing TASmax files"
#==============================================================================
for scen in "${scenarios[@]}"; do
    echo ${scen}
    for mod in "${models[@]}"; do
        echo ${mod}
        cd $inDIR/tasmax/${scen}/${mod}
        echo "taking annual min"
        for FILE in *; do cdo yearmin $FILE ${minoutDIR}/min_$FILE; done 
        echo "taking seasonal average"
        #winter in asia, europe, north america
        for FILE in *; do cdo -L selseas,DJF -seasmean  $FILE  ${avoutDIR}/DJF_$FILE; done
        #winter in south america, most of africa, australia
        for FILE in *; do cdo -L selseas,JJA -seasmean  $FILE  ${avoutDIR}/JJA_$FILE; done
    done
done

#==============================================================================
# get treeFrac for same time period as TAS
echo "processing treeFrac files"
#==============================================================================
for scen in "${scenarios[@]}"; do
    echo ${scen}
    for mod in "${models[@]}"; do
        echo ${mod}
        cd $inDIR/treeFrac/${scen}/${mod}
        # used average of the year, as data of coldest moth will be different for each pixel so can't select universally by date, 
        # and there is no seasonal forest cover pattern (decreases in what looks like an interpolation not a step function) so annual is good enough
        echo "taking annual average"
        for FILE in *; do cdo yearmean $FILE ${minoutDIR}/min_$FILE; done 
        echo "taking seasonal average"
        #winter in asia, europe, north america
        for FILE in *; do cdo -L selseas,DJF -seasmean  $FILE  ${avoutDIR}/DJF_$FILE; done 
        #winter in south america, most of africa, australia
        for FILE in *; do cdo -L selseas,JJA -seasmean  $FILE  ${avoutDIR}/JJA_$FILE; done
    done
done

#==============================================================================
# get snow depth for same time period as TAS
echo "processing snd files"
#==============================================================================
for scen in "${scenarios[@]}"; do
    echo ${scen}
    for mod in "${models[@]}"; do
        echo ${mod}
        cd $inDIR/snd/${scen}/${mod}
        echo "taking annual max"
        # similar to tree cover can't get one date corresponding to the min temp as all pixels different
        # choose annual max snow cover to correspond with annual min temp, although they may not occur at once 
        for FILE in *; do cdo yearmax  $FILE  ${minoutDIR}/min_$FILE; done
        echo "taking seasonal average"
        #winter in asia, europe, north america
        for FILE in *; do cdo -L selseas,DJF -seasmean  $FILE  ${avoutDIR}/DJF_$FILE; done
        #winter in south america, most of africa, australia
        for FILE in *; do cdo -L selseas,JJA -seasmean  $FILE  ${avoutDIR}/JJA_$FILE; done
    done
done

