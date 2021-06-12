#!/bin/bash

# See https://github.com/lehner/gpt/blob/master/lib/cgpt/update
# Original author Christoph Lehner

# configure warning
WARNING="This file is automatically generated, do not modify!"

# Automatically generate list of exported functions
(
    echo "// ${WARNING}" 
    sed -n 's/EXPORT(\([^,]*\),.*/EXPORT_FUNCTION(\1)/p' *.C
) > exports.h

echo "  Found $(grep -c EXPORT exports.h) exported functions"
echo "================================================================================"
