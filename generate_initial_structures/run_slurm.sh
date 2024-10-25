#!/bin/bash
#SBATCH --job-name=leo_gst_free
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --output=slurm.out
#SBATCH --error=slurm.err
#SBATCH --time=48:00:00
#SBATCH --cluster=invest
#SBATCH --partition=lchong
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=lel178@pitt.edu

module purge
module load gcc/8.2.0 openmpi/4.0.3
module load amber/20_cuda-11.1.1


pmemd.cuda -O -i prod.in -o prod1.out -p modified.prmtop -c eq.rst -r prod1.rst -x prod1.nc -inf prod1.nfo

pmemd.cuda -O -i prod.in -o prod2.out -p modified.prmtop -c prod1.rst -r prod2.rst -x prod2.nc -inf prod2.nfo

pmemd.cuda -O -i prod.in -o prod3.out -p modified.prmtop -c prod2.rst -r prod3.rst -x prod3.nc -inf prod3.nfo

pmemd.cuda -O -i prod.in -o prod4.out -p modified.prmtop  -c prod3.rst -r prod4.rst -x prod4.nc -inf prod4.nfo

pmemd.cuda -O -i prod.in -o prod5.out -p modified.prmtop -c prod4.rst -r prod5.rst -x prod5.nc -inf prod5.nfo

pmemd.cuda -O -i prod.in -o prod6.out -p modified.prmtop -c prod5.rst -r prod6.rst -x prod6.nc -inf prod6.nfo

pmemd.cuda -O -i prod.in -o prod7.out -p modified.prmtop -c prod6.rst -r prod7.rst -x prod7.nc -inf prod7.nfo

pmemd.cuda -O -i prod.in -o prod8.out -p modified.prmtop -c prod7.rst -r prod8.rst -x prod8.nc -inf prod8.nfo

pmemd.cuda -O -i prod.in -o prod9.out -p modified.prmtop -c prod8.rst -r prod9.rst -x prod9.nc -inf prod9.nfo

pmemd.cuda -O -i prod.in -o prod10.out -p modified.prmtop -c prod9.rst -r prod10.rst -x prod10.nc -inf prod10.nfo
