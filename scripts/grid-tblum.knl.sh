#!/bin/bash

. scripts/conf.sh

name=Grid-tblum

{

echo "!!!! build $name !!!!"

mkdir -p "$prefix"/$name || true

rsync -avr --delete $distfiles/$name/ "$prefix"/$name/

cd "$prefix/$name"

INITDIR="$(pwd)"
rm -rfv "${INITDIR}/Eigen/Eigen/unsupported"
rm -rfv "${INITDIR}/Grid/Eigen"
ln -vs "${INITDIR}/Eigen/Eigen" "${INITDIR}/Grid/Eigen"
ln -vs "${INITDIR}/Eigen/unsupported/Eigen" "${INITDIR}/Grid/Eigen/unsupported"

export CXXFLAGS="$CXXFLAGS -DUSE_QLATTICE"

mkdir build
cd build
../configure \
    --enable-simd=KNL \
    --enable-alloc-align=4k \
    --enable-comms=mpi-auto \
    --enable-mkl \
    --enable-shm=shmget \
    --enable-shmpath=/dev/hugepages \
    --enable-gparity=no \
    --with-lime="$prefix" \
    --with-hdf5="$prefix" \
    --with-fftw="$prefix" \
    --prefix="$prefix/grid-tblum"

make -j$num_proc
make install

cd $wd
echo "!!!! $name build !!!!"

rm -rf $temp_dir || true

} |& tee $prefix/log.$name.txt
