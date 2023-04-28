#!/bin/bash

#SBATCH --job-name=4_ensembleaverages
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --mem=16G
#SBATCH --mail-type=FAIL,END-user=Eva.Victoria.Marcy@vub.ac.be
#SBATCH --output out_4_ensembleaverages
#SBATCH --error err_4_ensembleaverages

echo Start Job
date

cd /scratch/brussel/105/vsc10501/thesis/scripts
echo "loading CDO module"
module load CDO/2.0.5-gompi-2021b
echo "running script"
./4_ensembleaverages.sh

echo End Job
