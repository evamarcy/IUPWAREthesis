#!/bin/bash

#SBATCH --job-name=1_makeworkingcopy
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --mail-type=FAIL,END-user=Eva.Victoria.Marcy@vub.ac.be
#SBATCH --output out_1_makeworkingcopy
#SBATCH --error err_1_makeworkingcopy

echo Start Job
date

cd /scratch/brussel/105/vsc10501/thesis/scripts
module load CDO/2.0.5-gompi-2021b
./1_makeworkingcopy.sh

echo End Job
