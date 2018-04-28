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

function gen_cpplib_wrapper
{
local specprof_path=$1
shift
local origin_lib_path=$1
shift
local target_function=$1
shift
local working_dir=$1
shift
local namespace=$1
shift
local includes=$@
echo -e "---------------------------------------------------------"
echo -e "Generating the C++ library that will profile the function"
CMD="${specprof_path} -o ${origin_lib_path} -s '"${target_function}"' -w ${working_dir} -n ${namespace} -i ${includes}"
echo -e $CMD
eval $CMD &> ${working_dir}/gen_c++lib_wrapper_output.txt
if [ $? != 0 ]; then
    echo -e "Unable to generate the wrapper around libtest_move_semantics.so!"
    cat ${working_dir}/gen_c++lib_wrapper_output.txt
    exit 5
fi
}

#function gen_cpplib_wrapper_bis
#{
#echo -e "-------------------------------------"
#echo -e "Generating the C++ library that will profile the method computeSum of the VectorWithoutMoveSem class in the
#namespace move_semantics_test in the libvector.so library"
#CMD="./src/spec_prof.py -o $CPP_EXAMPLE_DIR/libvector.so   -s 'double VectorWithoutMoveSem::computeSum() const' -w $WORKING_DIR -n move_semantics_test  -i $CPP_EXAMPLE_DIR/vector_without_move_sem.h"
#echo -e $CMD
#eval $CMD &> /dev/null
#if [ $? != 0 ]; then
#    echo -e "Unable to generate the wrapper around libtest_move_semantics.so!"
#    exit 6
#fi
#}

function main
{
local this_dir=$(pwd)
local working_dir="/tmp/specprof_wdir"
local cpp_example_dir="${this_dir}/C++_example/MoveSemantics"
local namespace="test_functions"

gen_executable ${cpp_example_dir}
create_working_directory ${working_dir}
gen_cpplib_wrapper ${this_dir}/src/spec_prof.py ${cpp_example_dir}/libtest_move_semantics.so 'void testReturnValueOptimization(const move_semantics_test::VectorWithMoveSem& vec_a,const move_semantics_test::VectorWithMoveSem& vec_b);' ${working_dir} ${namespace} ${cpp_example_dir}/vector_with_move_sem.h ${cpp_example_dir}/test_move_semantics.h
}

main
