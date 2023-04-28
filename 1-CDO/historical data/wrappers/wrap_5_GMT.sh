#!/bin/bash

#SBATCH --job-name=5_GMT
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --mem=16G
#SBATCH --mail-type=FAIL,END-user=Eva.Victoria.Marcy@vub.ac.be
#SBATCH --output out_5_GMT
#SBATCH --error err_5_GMT

echo Start Job
date

cd /scratch/brussel/105/vsc10501/thesis/scripts/historical/
echo "loading CDO module"
module load CDO/2.0.5-gompi-2021b
echo "running script"
./5_GMT.sh

echo End Job
