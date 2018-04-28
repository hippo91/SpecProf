#!/bin/bash
target_lib=$1
mangled_names=$(nm ${target_lib} | grep " U " |gawk '{print $2}')

for mangled_name in ${mangled_names}; do
    demangled_name=$(c++filt -it $mangled_name)
    if [ $? == 0 ]; then
        echo "$mangled_name ==> $demangled_name";
    fi
done

