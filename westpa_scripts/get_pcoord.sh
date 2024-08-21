#!/bin/bash
set -x
cat $WEST_STRUCT_DATA_REF/pcoord.init > $WEST_PCOORD_RETURN 

cp $WEST_SIM_ROOT/common_files/free.prmtop $WEST_TRAJECTORY_RETURN
cp $WEST_STRUCT_DATA_REF/bstate.ncrst $WEST_TRAJECTORY_RETURN

cp $WEST_SIM_ROOT/common_files/free.prmtop $WEST_RESTART_RETURN
cp $WEST_STRUCT_DATA_REF/bstate.ncrst $WEST_RESTART_RETURN/parent.ncrst
