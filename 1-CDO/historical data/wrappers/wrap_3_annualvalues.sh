#!/bin/bash

#SBATCH --job-name=3_annualvalues
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --mail-type=FAIL,END-user=Eva.Victoria.Marcy@vub.ac.be
#SBATCH --output out_3_annualvalues
#SBATCH --error err_3_annualvalues

echo Start Job
date

cd /scratch/brussel/105/vsc10501/thesis/scripts
module load CDO/2.0.5-gompi-2021b
./3_annualvalues.sh

echo End Job
