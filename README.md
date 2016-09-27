# SpecProf
A python application that generates a wrapper library able to count and measure execution times of a specific function in a shared object.

# Description

SpecProf is used to profile a specific function in a shared library, hereafter named target library, by making use of dlsym function.
There is no need to compile this target library with specific flags and of course no need to modify the source code.
SpecProf generates a C or C++ source file, depending on the language used to build the target library, and compiles it into a shared library that
wrapps the call of the function in the target library

# Usage

We want to profile the function named **computePressure** in the shared library under the path **/path/to/libcompute_hydrodynamics.so**. The complete signature
of the function is :

**void computePressure(const MySpecialObject&, double* datas, int param);**

We just have to run :

`./spec_prof.py -o /path/to/libcompute_hydrodynamics.so -s "void computePressure(const MySpecialObject&, double* datas, int param)" -w /tmp/working_dir -i /path/to/header/my_special_object.h`

**-o** : Indicates path to the target library (mandatory)

**-s** : The signature of the function or method to profile (mandatory)

**-w** : path to the directory where spec_prof will generate the source file and the shared library wrapper (mandatory)

**-i** : path to header files containing the definition of the objects types appearing in the function signature (optional)

SpecProf will generate a file named **libcompute_hydrodynamics_wrapper.cpp** and a shared object **libcompute_hydrodynamics_wrapper.so** in the /tmp/working_dir directory. 

# Postscript

Once generated, the shared library wrapper is used thanks to the following command :

`LD_PRELOAD=/tmp/working_dir/libcompute_hydrodynamics_wrapper.so /path/to/executable/using/the/target/library`

# Prerequisites

Standard unix/linux tools such as **ldd**, **nm** and a compilator able to deal with C++2011 are required.
