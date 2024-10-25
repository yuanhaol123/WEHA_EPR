#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF
tempF=$(awk -v "iter=$WEST_CURRENT_ITER" 'NR==iter' $WEST_SIM_ROOT/common_files/temp.dat | awk '{print $2}')
python $WEST_SIM_ROOT/common_files/modify_data_with_lambda.py $tempF $WEST_SIM_ROOT/common_files/free.prmtop ./modified.prmtop
#python $WEST_SIM_ROOT/common_files/modify_data_with_lambda.py $tempF $WEST_SIM_ROOT/common_files/p1_nowat.prmtop ./p1_nowat_mod.prmtop


ln -sv $WEST_SIM_ROOT/common_files/free.prmtop .
ln -sv $WEST_SIM_ROOT/common_files/modified.prmtop .

#echo $WEST_PARENT_DATA_REF

if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/test.in > test.in
#  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.in > md.in
  ln -sv $WEST_PARENT_DATA_REF/seg.ncrst ./parent.ncrst
elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/test.in > test.in
  #sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.in > md.in
  ln -sv $WEST_PARENT_DATA_REF/bstate.ncrst ./parent.ncrst
fi

export CUDA_DEVICES=(`echo $CUDA_VISIBLE_DEVICES_ALLOCATED | tr , ' '`)
export CUDA_VISIBLE_DEVICES=${CUDA_DEVICES[$WM_PROCESS_INDEX]}

echo "RUNSEG.SH: CUDA_VISIBLE_DEVICES_ALLOCATED = " $CUDA_VISIBLE_DEVICES_ALLOCATED
echo "RUNSEG.SH: WM_PROCESS_INDEX = " $WM_PROCESS_INDEX
echo "RUNSEG.SH: CUDA_VISIBLE_DEVICES = " $CUDA_VISIBLE_DEVICES


#tempP=$(awk -v "iter=$WEST_CURRENT_ITER" 'NR==iter' $WEST_SIM_ROOT/common_files/temp.dat | awk '{print $2}')
tempF=$(awk -v "iter=$WEST_CURRENT_ITER" 'NR==iter' $WEST_SIM_ROOT/common_files/temperature.dat | awk '{print $2}')

echo $tempF $WEST_SIM_ROOT


rm sa
echo " temp0 = ${tempF}," >> sa
echo "&end" >> sa
echo " " >> sa

cat test.in sa > md.in
rm sa

$PMEMD  -O -i md.in   -p modified.prmtop -c parent.ncrst \
           -r seg.ncrst -x seg.nc      -o seg.log    -inf seg.nfo

DIST=$(mktemp)
COMMAND="         parm free.prmtop\n"
COMMAND="$COMMAND trajin $WEST_CURRENT_SEG_DATA_REF/parent.ncrst\n"
COMMAND="$COMMAND trajin $WEST_CURRENT_SEG_DATA_REF/seg.nc\n"
#COMMAND="$COMMAND reference $WEST_SIM_ROOT/common_files/reference.pdb \n" 
COMMAND="$COMMAND autoimage \n"
COMMAND="$COMMAND strip :WAT,Na+,Cl- \n"
COMMAND="$COMMAND distance @7275 @7317 noimage out $DIST \n"
COMMAND="$COMMAND energy  :1-444 out energy.dat \n"
#COMMAND="$COMMAND rms reference :1-442 \n"
#COMMAND="$COMMAND rms reference :1-442@CA nofit out rmsd.dat \n"
COMMAND="$COMMAND trajout nowater.nc \n"
COMMAND="$COMMAND go\n"

echo -e $COMMAND | $CPPTRAJ
cat $DIST | tail -n +2 | awk {'print $2'} > $WEST_PCOORD_RETURN
cat energy.dat | tail -n +2 | awk '{print $4}' > $WEST_DIH_ENERGY_RETURN
cat energy.dat | tail -n +2 | awk '{print ($5 + $7)}' > $WEST_VDW_ENERGY_RETURN
cat energy.dat | tail -n +2 | awk '{print ($6 + $8)}' > $WEST_ELEC_ENERGY_RETURN
python $WEST_SIM_ROOT/common_files/get_energy.py > $WEST_ENERGY_RETURN
#cat $RMSD | tail -n +2 | awk {'print $2 , $3'} > $WEST_AUX_RETURN


#cp free.prmtop $WEST_TRAJECTORY_RETURN
#cp seg.nc $WEST_TRAJECTORY_RETURN
#
#cp free.prmtop $WEST_RESTART_RETURN
#cp seg.ncrst $WEST_RESTART_RETURN/parent.ncrst

#cp seg.log $WEST_LOG_RETURN

#rm free.prmtop seg.nc
