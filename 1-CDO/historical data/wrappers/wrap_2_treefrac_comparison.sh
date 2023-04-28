#!/bin/bash

#SBATCH --job-name=2_treefrac_comparison
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --mail-type=FAIL,END-user=Eva.Victoria.Marcy@vub.ac.be
#SBATCH --output out_2_treefrac_comparison
#SBATCH --error err_2_treefrac_comparison

echo Start Job
date

cd /scratch/brussel/105/vsc10501/thesis/scripts
module load CDO/2.0.5-gompi-2021b
./2_treefrac_comparison.sh

echo End Job
