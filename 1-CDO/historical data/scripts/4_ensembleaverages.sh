#!/bin/bash -l

# =============================================================================
# SUMMARY
# =============================================================================

# Code to take ensemble averages for each model and multimodel averages
# does averages with both: all available realizations AND pairwise realizations only

# =============================================================================

#define lists for iteration
variables=("tas" "tasmax" "treeFrac" "snd")
variables_tsteps=("Amon" "Lmon" "LImon")
scenarios=("hist-noLu" "historical")
projects=("LUMIP" "CMIP")
models=("CanESM5" "CNRM-ESM2-1" "IPSL-CM6A-LR" "UKESM1-0-LL")
models_noUKESM=("CanESM5" "CNRM-ESM2-1" "IPSL-CM6A-LR")


#create folders
mkdir $WORKDIR/thesis/data/ensembles/
for var in "${variables[@]}"; do
    mkdir $WORKDIR/thesis/data/ensembles/${var}
    for scen in "${scenarios[@]}"; do
        mkdir $WORKDIR/thesis/data/ensembles/${var}/${scen}
    done
done

# =============================================================================
# all available realizations
# =============================================================================

# =============================================================================
### take ensemble average for all files for each model for each scenario and each variable, except UKESM since the time periods are wrong
for var in "${variables[@]}"; do
    echo ${var}
    for scen in "${scenarios[@]}"; do
        echo ${scen}
        for mod in "${models_noUKESM[@]}"; do
            echo ${mod}
            cdo ensmean /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/*/*/${mod}/${scen}/*/*/${var}/*/*/${var}_*_${mod}_${scen}_*.nc $WORKDIR/thesis/data/ensembles/${var}/${scen}/ensembleav_${var}_${scen}_${mod}.nc
        done
    done
done

# =============================================================================
#take ensemble average for all files for each model for each scenario and each variable for UKESM

mod="UKESM1-0-LL"
echo $mod

#first make a time merged copy of all UKESM files to keep in working directory
mod="UKESM1-0-LL"
echo $mod
mkdir $WORKDIR/thesis/data/UKESM/
for i in "${!variables[@]}"; do
    echo ${variables[i]}
    mkdir $WORKDIR/thesis/data/UKESM/${variables[i]}/
    for j in "${!scenarios[@]}"; do
        echo ${scenarios[j]}
        mkdir $WORKDIR/thesis/data/UKESM/${variables[i]}/${scenarios[j]}/
        cd /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/${projects[j]}/MOHC/${mod}/${scenarios[j]}/
        for r in * ; do 
            cdo mergetime ${r}/${variables_tsteps[i]}/${variables[i]}/gn/*/${variables[i]}_${variables_tsteps[i]}_${mod}_${scenarios[j]}_r*_gn_185001-194912.nc ${r}/${variables_tsteps[i]}/${variables[i]}/gn/*/${variables[i]}_${variables_tsteps[i]}_${mod}_${scenarios[j]}_r*_gn_195001-201412.nc $WORKDIR/thesis/data/UKESM/${variables[i]}/${scenarios[j]}/${variables[i]}_${variables_tsteps[i]}_${mod}_${scenarios[j]}_${r}_gn_185001-202012.nc
        done
    done
done


#then get ensemble mean for each scenario and each variable
for var in "${variables[@]}"; do
    echo ${var}
    for scen in "${scenarios[@]}"; do
        echo ${scen}
        cdo ensmean  $WORKDIR/thesis/data/UKESM/${var}/${scen}/${var}_*_${mod}_${scen}_*_gn_185001-202012.nc $WORKDIR/thesis/data/ensembles/${var}/${scen}/ensembleav_${var}_${scen}_${mod}.nc
    done
done


# =============================================================================
#Get annual values
mkdir $WORKDIR/thesis/data/annualmin/ensemble_allrealizations
mkdir $WORKDIR/thesis/data/winteraverage/ensemble_allrealizations

for mod in "${models[@]}"; do
    echo ${mod}
    for scen in "${scenarios[@]}"; do
        echo ${scen}
        
        # take annual min max and average for tas, snd and treeFrac respectively
        echo "tas annual min"
        cdo yearmin $WORKDIR/thesis/data/ensembles/tas/${scen}/ensembleav_tas_${scen}_${mod}.nc $WORKDIR/thesis/data/annualmin/ensemble_allrealizations/min_ensembleav_tas_${scen}_${mod}.nc
        echo "tasmax annual min"
        cdo yearmin $WORKDIR/thesis/data/ensembles/tasmax/${scen}/ensembleav_tasmax_${scen}_${mod}.nc $WORKDIR/thesis/data/annualmin/ensemble_allrealizations/min_ensembleav_tasmax_${scen}_${mod}.nc
        echo "snd annual max"
        cdo yearmax $WORKDIR/thesis/data/ensembles/snd/${scen}/ensembleav_snd_${scen}_${mod}.nc $WORKDIR/thesis/data/annualmin/ensemble_allrealizations/min_ensembleav_snd_${scen}_${mod}.nc
        echo "treeFrac annual average"
        cdo yearmean $WORKDIR/thesis/data/ensembles/treeFrac/${scen}/ensembleav_treeFrac_${scen}_${mod}.nc $WORKDIR/thesis/data/annualmin/ensemble_allrealizations/min_ensembleav_treeFrac_${scen}_${mod}.nc
        
        # take winter average for all variables, north and south hemisphere
        echo "winter averages"
        for var in "${variables[@]}"; do
            echo ${var}
            cdo -L selseas,JJA -seasmean $WORKDIR/thesis/data/ensembles/${var}/${scen}/ensembleav_${var}_${scen}_${mod}.nc $WORKDIR/thesis/data/winteraverage/ensemble_allrealizations/JJA_ensembleav_${var}_${scen}_${mod}.nc 
            cdo -L selseas,DJF -seasmean $WORKDIR/thesis/data/ensembles/${var}/${scen}/ensembleav_${var}_${scen}_${mod}.nc $WORKDIR/thesis/data/winteraverage/ensemble_allrealizations/DJF_ensembleav_${var}_${scen}_${mod}.nc
        done

    done
done


# =============================================================================
# regrid the ensemble averages to match all the same grid 
cd $WORKDIR/thesis/data/winteraverage/ensemble_allrealizations/
pwd
for file in *; do
    cdo remapbil,JJA_ensembleav_treeFrac_historical_CanESM5.nc ${file} regrid_${file}
done

cd $WORKDIR/thesis/data/annualmin/ensemble_allrealizations/
pwd
for file in *; do
    cdo remapbil,min_ensembleav_treeFrac_historical_CanESM5.nc ${file} regrid_${file}
done


# =============================================================================
# take the multimodel average and then remove the regrid copies
for var in "${variables[@]}"; do
    echo ${var}
    for scen in "${scenarios[@]}"; do
        echo ${scen}
        cd $WORKDIR/thesis/data/winteraverage/ensemble_allrealizations/
        cdo ensmean regrid_JJA_ensembleav_${var}_${scen}_*.nc JJA_multimodelav_${var}_${scen}.nc
        cdo ensmean regrid_DJF_ensembleav_${var}_${scen}_*.nc DJF_multimodelav_${var}_${scen}.nc
        rm regrid_JJA_ensembleav_${var}_${scen}_*.nc
        rm regrid_DJF_ensembleav_${var}_${scen}_*.nc
        cd $WORKDIR/thesis/data/annualmin/ensemble_allrealizations/
        cdo ensmean regrid_min_ensembleav_${var}_${scen}_*.nc min_multimodelav_${var}_${scen}.nc
        rm regrid_min_ensembleav_${var}_${scen}_*.nc
    done
done

# =============================================================================
# pairwise realizations only
# =============================================================================

# =============================================================================
# take the ensemble mean for the pairwise realizations

mkdir $WORKDIR/thesis/data/annualmin/ensemble_pairwiserealizations
mkdir $WORKDIR/thesis/data/winteraverage/ensemble_pairwiserealizations


for var in "${variables[@]}"; do
    echo ${var}
    for scen in "${scenarios[@]}"; do
        echo ${scen}
        for mod in "${models[@]}"; do
            echo ${mod}
            cdo ensmean $WORKDIR/thesis/data/annualmin/individual_pairwiserealizations/min_${var}_*_${mod}_${scen}_*.nc $WORKDIR/thesis/data/annualmin/ensemble_pairwiserealizations/min_ensembleav_${var}_${scen}_${mod}.nc
            cdo ensmean $WORKDIR/thesis/data/winteraverage/individual_pairwiserealizations/JJA_${var}_*_${mod}_${scen}_*.nc $WORKDIR/thesis/data/winteraverage/ensemble_pairwiserealizations/JJA_ensembleav_${var}_${scen}_${mod}.nc
            cdo ensmean $WORKDIR/thesis/data/winteraverage/individual_pairwiserealizations/DJF_${var}_*_${mod}_${scen}_*.nc $WORKDIR/thesis/data/winteraverage/ensemble_pairwiserealizations/DJF_ensembleav_${var}_${scen}_${mod}.nc
        done
    done
done


# =============================================================================
# regrid the ensemble averages to match all the same grid 

cd $WORKDIR/thesis/data/annualmin/ensemble_pairwiserealizations/
for file in *; do
    cdo remapbil,min_ensembleav_treeFrac_historical_CanESM5.nc $file regrid_$file
done

for var in "${variables[@]}"; do
    echo ${var}
    for scen in "${scenarios[@]}"; do
        echo ${scen}
        cdo ensmean regrid_min_ensembleav_${var}_${scen}_*.nc min_multimodelav_${var}_${scen}.nc
    done
done
rm regrid*


cd $WORKDIR/thesis/data/winteraverage/ensemble_pairwiserealizations/
for file in *; do
    cdo remapbil,JJA_ensembleav_treeFrac_historical_CanESM5.nc $file regrid_$file
done

for var in "${variables[@]}"; do
    echo ${var}
    for scen in "${scenarios[@]}"; do
        echo ${scen}
        cdo ensmean regrid_JJA_ensembleav_${var}_${scen}_*.nc JJA_multimodelav_${var}_${scen}.nc
        cdo ensmean regrid_DJF_ensembleav_${var}_${scen}_*.nc DJF_multimodelav_${var}_${scen}.nc
    done
done
rm regrid*


