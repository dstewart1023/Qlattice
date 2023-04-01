#!/bin/bash

name=setenv-uconn

source qcore/set-prefix.sh

{ time {
    echo "!!!! build $name !!!!"
    source qcore/conf.sh

#
cat >"$prefix/setenv.sh" <<EOF
if [ -z "\$num_proc" ] ; then
    export num_proc=8
fi
source /etc/profile
module purge
module add gcc/11.3.0
module add openmpi/4.1.4
module list
# ``OMPI_MCA_pml=ucx'' does not work for mpi4py
export OMPI_MCA_pml=
EOF

    #
    "$wd"/qcore/bin/mk-setenv-dir.sh --keep
    echo "!!!! $name build !!!!"
} } 2>&1 | tee $prefix/log.$name.txt
