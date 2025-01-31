#!/bin/bash

set -e

{

./scripts/setenv.default.sh

./scripts/fftw_mpi.sh
./scripts/fftwf_mpi.sh
./scripts/cuba.sh
./scripts/zlib.sh
./scripts/eigen.sh
./scripts/qlat.sh

./scripts/c-lime.sh
./scripts/grid.gen16.sh
./scripts/gpt.sh

} |& tee $prefix/log.build.txt
