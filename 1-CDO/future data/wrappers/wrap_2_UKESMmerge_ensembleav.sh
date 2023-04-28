#!/bin/bash

#SBATCH --job-name=2_UKESMmerge_ensembleav
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --mem=16G
#SBATCH --mail-type=FAIL,END-user=Eva.Victoria.Marcy@vub.ac.be
#SBATCH --output out_2_UKESMmerge_ensembleav
#SBATCH --error err_2_UKESMmerge_ensembleav

echo Start Job
date

cd /scratch/brussel/105/vsc10501/thesis/scripts/future/
echo "loading CDO module"
module load CDO/2.0.6-gompi-2022a
echo "running script"
./2_UKESMmerge_ensembleav.sh

echo End Job
