#!/bin/bash
function gen_executable
{
local src_dir=$1
echo -e "------------------------------------------"
echo -e "Generating original executable and library"
cd ${src_dir}
if [ $? == 0 ]; then
  make LIBRARY=true
else
  echo -e "Unable to go the directory : ${src_dir}"
  exit 1
fi
}

function create_working_directory
{
local working_dir=$1
echo -e "-----------------------------------------------"
echo -e "Creating working directory under ${working_dir}"
mkdir -p ${working_dir}
if [ $? != 0 ]; then
    echo -e "Unable to create the ${working_dir} directory!"
    exit 3
fi
}

function gen_clib_wrapper
{
local specprof_path=$1
local origin_lib_path=$2
local target_function=$3
local working_dir=$4
echo -e "-------------------------------------------------------"
echo -e "Generating the C library that will profile the function"
#CMD="./src/spec_prof.py -o  $C_EXAMPLE_DIR/libtimewaster.so  -s 'void waste_time(int seconds);' -w $WORKING_DIR"
CMD="${specprof_path} -o  ${origin_lib_path}  -s '"${target_function}"' -w ${working_dir}"
echo -e $CMD
eval $CMD &> ${working_dir}/gen_clib_wrapper_output.txt
if [ $? != 0 ]; then
    echo -e "Unable to generate the wrapper around libtimewaster.so!"
    cat ${working_dir}/gen_clib_wrapper_output.txt
    exit 4
fi
}

function main
{
local this_dir=$(pwd)
local c_example_dir="${this_dir}/C_example/TimeWaster"
local working_dir="/tmp/specprof_wdir"
CPP_EXAMPLE_DIR="${this_dir}/C++_example/MoveSemantics"

gen_executable ${c_example_dir}
create_working_directory ${working_dir}
gen_clib_wrapper ${this_dir}/src/spec_prof.py ${c_example_dir}/libtimewaster.so 'void waste_time(int seconds);' ${working_dir}
}

main
