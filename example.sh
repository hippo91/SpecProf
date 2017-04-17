#!/bin/bash
THIS_DIR=$(pwd)
C_EXAMPLE_DIR="$THIS_DIR/C_example/TimeWaster"
CPP_EXAMPLE_DIR="$THIS_DIR/C++_example/MoveSemantics"
WORKING_DIR="/tmp/specprof_wdir"

echo -e "-------------------------------------"
echo -e "Generating C executable and library"
cd $C_EXAMPLE_DIR
if [ $? == 0 ]; then
  make LIBRARY=true
else
  echo -e "Unable to go the directory : $C_EXAMPLE_DIR"
fi
echo -e "-------------------------------------"
echo -e "Generating C++ executable and library"
cd $CPP_EXAMPLE_DIR
if [ $? == 0 ]; then
  make LIBRARY=true
else
  echo -e "Unable to go the directory : $CPP_EXAMPLE_DIR"
fi
echo -e "-------------------------------------"
echo -e "Creating working directory under $WORKING_DIR"
mkdir -p $WORKING_DIR
cd $THIS_DIR
echo -e "-------------------------------------"
echo -e "Generating the C library that will profile the function 'waste_time' in the libtimewaster library..."
CMD="./src/spec_prof.py -o  $C_EXAMPLE_DIR/libtimewaster.so  -s 'void waste_time(int seconds);' -w $WORKING_DIR"
echo -e $CMD
eval $CMD &> /dev/null
echo -e "-------------------------------------"
echo -e "Generating the C++ library that will profile the function testReturnValueOptimization in the namespace test_functions in the
libtest_move_semantics.so library"
CMD="./src/spec_prof.py -o $CPP_EXAMPLE_DIR/libtest_move_semantics.so   -s 'void testReturnValueOptimization(const move_semantics_test::VectorWithMoveSem& vec_a,const move_semantics_test::VectorWithMoveSem& vec_b);' -w $WORKING_DIR -n test_functions -i $CPP_EXAMPLE_DIR/vector_with_move_sem.h $CPP_EXAMPLE_DIR/test_move_semantics.h"
echo -e $CMD
eval $CMD &> /dev/null
echo -e "-------------------------------------"
echo -e "Generating the C++ library that will profile the method computeSum of the VectorWithoutMoveSem class in the
namespace move_semantics_test in the libvector.so library"
CMD="./src/spec_prof.py -o $CPP_EXAMPLE_DIR/libvector.so   -s 'double VectorWithoutMoveSem::computeSum() const' -w $WORKING_DIR -n move_semantics_test  -i $CPP_EXAMPLE_DIR/vector_without_move_sem.h"
echo -e $CMD
eval $CMD &> /dev/null
