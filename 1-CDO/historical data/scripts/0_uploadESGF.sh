#!/bin/bash -l

# =============================================================================
# SUMMARY
# =============================================================================

# Code to add missing files found on ESGF to the main file structure

# =============================================================================

# snd historical
realizations=("r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r5i1p1f1" "r10i1p1f1")
inDIR=$WORKDIR/thesis/data/raw_copy/snd/historical/CanESM5
for r in "${realizations[@]}"; do
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CCCma/CanESM5/historical/${r}/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CCCma/CanESM5/historical/${r}/LImon/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CCCma/CanESM5/historical/${r}/LImon/snd/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CCCma/CanESM5/historical/${r}/LImon/snd/gn/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CCCma/CanESM5/historical/${r}/LImon/snd/gn/v20190429/
    cp $inDIR/snd_LImon_CanESM5_historical_${r}_gn_185001-201412.nc /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/CMIP/CCCma/CanESM5/historical/${r}/LImon/snd/gn/v20190429/
done

# tas hist-noLu
realizations=("r2i1p1f1" "r8i1p1f1")
inDIR=$WORKDIR/thesis/data/raw_copy/tas/hist-noLu/CanESM5
for r in "${realizations[@]}"; do
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/Amon/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/Amon/tas/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/Amon/tas/gn/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/Amon/tas/gn/v20190429/
    cp $inDIR/tas_Amon_CanESM5_hist-noLu_${r}_gn_185001-202012.nc /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/Amon/tas/gn/v20190429/
done

# tasmax hist-noLu
realizations=("r1i1p1f1" "r4i1p1f1" "r5i1p1f1")
inDIR=$WORKDIR/thesis/data/raw_copy/tasmax/hist-noLu/CanESM5
for r in "${realizations[@]}"; do
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/Amon/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/Amon/tasmax/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/Amon/tasmax/gn/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/Amon/tasmax/gn/v20190429/
    cp $inDIR/tasmax_Amon_CanESM5_hist-noLu_${r}_gn_185001-202012.nc /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CCCma/CanESM5/hist-noLu/${r}/Amon/tasmax/gn/v20190429/
done

realizations=("r2i1p1f2" "r3i1p1f2")
inDIR=$WORKDIR/thesis/data/raw_copy/tasmax/hist-noLu/CNRM-ESM2-1
for r in "${realizations[@]}"; do
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CNRM-CERFACS/CNRM-ESM2-1/hist-noLu/${r}/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CNRM-CERFACS/CNRM-ESM2-1/hist-noLu/${r}/Amon/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CNRM-CERFACS/CNRM-ESM2-1/hist-noLu/${r}/Amon/tasmax/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CNRM-CERFACS/CNRM-ESM2-1/hist-noLu/${r}/Amon/tasmax/gr/
    mkdir /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CNRM-CERFACS/CNRM-ESM2-1/hist-noLu/${r}/Amon/tasmax/gr/v20200923/
    cp $inDIR/tasmax_Amon_CNRM-ESM2-1_hist-noLu_${r}_gr_185001-201412.nc /vscmnt/brussel_pixiu_data/_data_brussel/vo/000/bvo00012/data/dataset/cmip6/LUMIP/CNRM-CERFACS/CNRM-ESM2-1/hist-noLu/${r}/Amon/tasmax/gr/v20200923/
done