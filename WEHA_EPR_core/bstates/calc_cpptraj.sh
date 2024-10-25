#!/bin/bash

ii=1
for BS in 01 02 03 04 05 06 07 08 09 10
do
    mkdir ${BS}
    #cp file.ncrst.${ii} ${BS}/bstate.ncrst
    mv prod${ii}.rst ${BS}/bstate.ncrst
    echo $i

    cd ${BS}
    COMMAND="         parm ../../common_files/free.prmtop\n"
    COMMAND="$COMMAND trajin bstate.ncrst \n"
    COMMAND="$COMMAND autoimage \n"
    COMMAND="$COMMAND distance @7275 @7317 out dist.dat noimage \n"
    COMMAND="$COMMAND energy  :1-444 out energy.dat \n"
    COMMAND="$COMMAND go\n"
    echo -e $COMMAND | cpptraj
    
    awk 'NR>1' dist.dat | awk '{print $2}' > pcoord.init
    cat energy.dat | tail -n +2 | awk '{print $10 }' >> ../energy.dat 
    rm dist.dat
    ii=$(($ii+1))
    
    cd ..
done
echo $ii
