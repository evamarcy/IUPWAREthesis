#!/bin/bash -l

# =============================================================================
# SUMMARY
# =============================================================================

# Code to copy files from CMIP6 folder to working directory

# =============================================================================

#name output directory
dirname=raw_copy

#define lists for iteration
variables=("tas" "treeFrac" "snd")
scenarios=("hist-noLu" "historical")
models=("CanESM5" "CNRM-ESM2-1" "IPSL-CM6A-LR" "UKESM1-0-LL")


#create folders
mkdir $WORKDIR/thesis/data/${dirname}/
for var in "${variables[@]}"; do
    mkdir $WORKDIR/thesis/data/${dirname}/${var}
    for scen in "${scenarios[@]}"; do
        mkdir $WORKDIR/thesis/data/${dirname}/${var}/${scen}
        for mod in "${models[@]}"; do
        mkdir $WORKDIR/thesis/data/${dirname}/${var}/${scen}/${mod}
        done
    done
done


#copy data over to working directory for each model
mod="CanESM5"
#r2 and r8 not in hist-noLu, were removed after the fact, should be updated in future versions
realizations=("r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r5i1p1f1" "r6i1p1f1" "r7i1p1f1" "r8i1p1f1" "r9i1p1f1" "r10i1p1f1")
for r in "${realizations[@]}"; do
    #tas
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/${mod}/hist-noLu/${r}/Amon/tas/gn/*/tas_Amon_${mod}_hist-noLu_${r}_gn_185001-202012.nc $WORKDIR/thesis/data/${dirname}/tas/hist-noLu/${mod}/
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CCCma/${mod}/historical/${r}/Amon/tas/gn/*/tas_Amon_${mod}_historical_${r}_gn_185001-201412.nc $WORKDIR/thesis/data/${dirname}/tas/historical/${mod}/
    #snow depth 
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/${mod}/hist-noLu/${r}/LImon/snd/gn/*/snd_LImon_${mod}_hist-noLu_${r}_gn_185001-202012.nc $WORKDIR/thesis/data/${dirname}/snd/hist-noLu/${mod}/
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CCCma/${mod}/historical/${r}/LImon/snd/gn/*/snd_LImon_${mod}_historical_${r}_gn_185001-201412.nc $WORKDIR/thesis/data/${dirname}/snd/historical/${mod}/
    #treeFrac
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CCCma/${mod}/historical/${r}/Lmon/treeFrac/gn/*/treeFrac_Lmon_${mod}_historical_${r}_gn_185001-201412.nc $WORKDIR/thesis/data/${dirname}/treeFrac/historical/${mod}/
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/${mod}/hist-noLu/${r}/Lmon/treeFrac/gn/*/treeFrac_Lmon_${mod}_hist-noLu_${r}_gn_185001-201412.nc $WORKDIR/thesis/data/${dirname}/treeFrac/hist-noLu/${mod}/
done


mod="CNRM-ESM2-1"
realizations=("r1i1p1f2" "r2i1p1f2" "r3i1p1f2")
for r in "${realizations[@]}"; do
    #tas
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CNRM-CERFACS/${mod}/hist-noLu/${r}/Amon/tas/gr/*/tas_Amon_${mod}_hist-noLu_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/tas/hist-noLu/${mod}/
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CNRM-CERFACS/${mod}/historical/${r}/Amon/tas/gr/*/tas_Amon_${mod}_historical_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/tas/historical/${mod}/
    #snow depth 
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CNRM-CERFACS/${mod}/hist-noLu/${r}/LImon/snd/gr/*/snd_LImon_${mod}_hist-noLu_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/snd/hist-noLu/${mod}/
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CNRM-CERFACS/${mod}/historical/${r}/LImon/snd/gr/*/snd_LImon_${mod}_historical_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/snd/historical/${mod}/
    #treeFrac
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CNRM-CERFACS/${mod}/historical/${r}/Lmon/treeFrac/gr/*/treeFrac_Lmon_${mod}_historical_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/treeFrac/historical/${mod}/
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CNRM-CERFACS/${mod}/hist-noLu/${r}/Lmon/treeFrac/gr/*/treeFrac_Lmon_${mod}_hist-noLu_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/treeFrac/hist-noLu/${mod}/
done

mod="IPSL-CM6A-LR"
realizations=("r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1")
for r in "${realizations[@]}"; do
    #tas
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/IPSL/${mod}/hist-noLu/${r}/Amon/tas/gr/*/tas_Amon_${mod}_hist-noLu_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/tas/hist-noLu/${mod}/
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/IPSL/${mod}/historical/${r}/Amon/tas/gr/*/tas_Amon_${mod}_historical_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/tas/historical/${mod}/
    #snow depth 
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/IPSL/${mod}/hist-noLu/${r}/LImon/snd/gr/*/snd_LImon_${mod}_hist-noLu_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/snd/hist-noLu/${mod}/
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/IPSL/${mod}/historical/${r}/LImon/snd/gr/*/snd_LImon_${mod}_historical_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/snd/historical/${mod}/
    #treeFrac
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/IPSL/${mod}/hist-noLu/${r}/Lmon/treeFrac/gr/*/treeFrac_Lmon_${mod}_hist-noLu_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/treeFrac/hist-noLu/${mod}/
    cp /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/IPSL/${mod}/historical/${r}/Lmon/treeFrac/gr/*/treeFrac_Lmon_${mod}_historical_${r}_gr_185001-201412.nc $WORKDIR/thesis/data/${dirname}/treeFrac/historical/${mod}/
done

mod="UKESM1-0-LL"
realizations=("r1i1p1f2" "r2i1p1f2" "r3i1p1f2" "r4i1p1f2")
for r in "${realizations[@]}"; do
    #tas
    cd /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/MOHC/${mod}/hist-noLu/${r}/Amon/tas/gn/*/
    cdo mergetime tas_Amon_${mod}_hist-noLu_${r}_gn_185001-194912.nc tas_Amon_${mod}_hist-noLu_${r}_gn_195001-201412.nc $WORKDIR/thesis/data/${dirname}/tas/hist-noLu/${mod}/tas_Amon_${mod}_hist-noLu_${r}_gn_185001-202012.nc

    cd /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/MOHC/${mod}/historical/${r}/Amon/tas/gn/*/
    cdo mergetime tas_Amon_${mod}_historical_${r}_gn_185001-194912.nc tas_Amon_${mod}_historical_${r}_gn_195001-201412.nc $WORKDIR/thesis/data/${dirname}/tas/historical/${mod}/tas_Amon_${mod}_historical_${r}_gn_185001-202012.nc
    
    #snow depth 
    cd /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/MOHC/${mod}/hist-noLu/${r}/LImon/snd/gn/*/
    cdo mergetime snd_LImon_${mod}_hist-noLu_${r}_gn_185001-194912.nc snd_LImon_${mod}_hist-noLu_${r}_gn_195001-201412.nc $WORKDIR/thesis/data/${dirname}/snd/hist-noLu/${mod}/snd_LImon_${mod}_hist-noLu_${r}_gn_185001-202012.nc
    
    cd /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/MOHC/${mod}/historical/${r}/LImon/snd/gn/*/
    cdo mergetime snd_LImon_${mod}_historical_${r}_gn_185001-194912.nc snd_LImon_${mod}_historical_${r}_gn_195001-201412.nc $WORKDIR/thesis/data/${dirname}/snd/historical/${mod}/snd_LImon_${mod}_historical_${r}_gn_185001-202012.nc
    
    #treeFrac
    cd /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/MOHC/${mod}/historical/${r}/Lmon/treeFrac/gn/*/
    cdo mergetime treeFrac_Lmon_${mod}_historical_${r}_gn_185001-194912.nc treeFrac_Lmon_${mod}_historical_${r}_gn_195001-201412.nc $WORKDIR/thesis/data/${dirname}/treeFrac/historical/${mod}/treeFrac_Lmon_${mod}_historical_${r}_gn_185001-202012.nc

    cd /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/MOHC/${mod}/hist-noLu/${r}/Lmon/treeFrac/gn/*/
    cdo mergetime treeFrac_Lmon_${mod}_hist-noLu_${r}_gn_185001-194912.nc treeFrac_Lmon_${mod}_hist-noLu_${r}_gn_195001-201412.nc $WORKDIR/thesis/data/${dirname}/treeFrac/hist-noLu/${mod}/treeFrac_Lmon_${mod}_hist-noLu_${r}_gn_185001-202012.nc
done

