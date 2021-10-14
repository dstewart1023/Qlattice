#!/bin/bash

./scripts/setenv-jlabknl.sh

./scripts/fftw.sh
./scripts/fftwf.sh
./scripts/cuba.sh
./scripts/zlib.sh
./scripts/eigen.sh
./scripts/qlat.sh

./scripts/autoconf.sh
./scripts/automake.sh
./scripts/c-lime.sh
./scripts/hdf5.sh
./scripts/grid-tblum-knl.sh
./scripts/hadrons-tblum-knl.sh
./scripts/grid-knl.sh
./scripts/gpt.sh