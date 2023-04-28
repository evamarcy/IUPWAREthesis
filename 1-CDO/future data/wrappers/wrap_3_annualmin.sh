#!/bin/bash

#SBATCH --job-name=3_annualmin
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --mem=16G
#SBATCH --mail-type=FAIL,END-user=Eva.Victoria.Marcy@vub.ac.be
#SBATCH --output out_3_annualmin
#SBATCH --error err_3_annualmin

echo Start Job
date

cd /scratch/brussel/105/vsc10501/thesis/scripts/future/
echo "loading CDO module"
module load CDO/2.0.6-gompi-2022a
echo "running script"
./3_annualmin.sh

echo End Job
