// Mandatory includes
#include <iostream>
#include <exception>
#include <string>
#include <chrono>
#include <string.h>
#include <stdlib.h>
// necessary for RTLD_NEXT in dlfcn.h
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <dlfcn.h>

// --------------------------------------------------------------
// -- Optional includes
// --------------------------------------------------------------


#include "/home/guillaume2/Informatique/Programmation/cpp/move-semantics-tst/vector_without_move_sem.h"



// --------------------------------------------------------------
// -- GLOBAL VARIABLES
// --------------------------------------------------------------

typedef double (move_semantics_test::VectorWithoutMoveSem::*func_ptr)() const;

// Target library path
static const char *target_library = "/home/guillaume2/Informatique/Programmation/cpp/move-semantics-tst/libvector.so";
// Target symbol
static const char *target_symbol = "_ZNK19move_semantics_test20VectorWithoutMoveSem10computeSumEv";
// Specific pointer to function type


// Address of the target function will be stored in :
static func_ptr orig_func(nullptr);
// Total number of calls
static long int call_count(0);
// Cumulative time used by the function
static std::chrono::microseconds total_time_used;

// --------------------------------------------------------------
// -- FUNCTIONS
// --------------------------------------------------------------

//Library Initializer
void __attribute__((constructor)) setup()
{
    if (orig_func == nullptr) {
        std::cout << "***********************************************" << std::endl;
        std::cout << "Call of the library initializer!" << std::endl;
        void *handle;  // Handle of the target library
        dlerror();  // Cleaning of potential previous error message
        std::cout << "Trying to open the target library...";
        handle = dlopen(target_library, RTLD_LAZY);
        std::cout << "...done!" << std::endl;
        if (!handle) {
            std::cout << "Unable to access origin library!" << std::endl;
            std::cerr << dlerror() << std::endl;
            std::terminate();
        } else {
            std::cout << "Library " << target_library << " found and opened successfully!" << std::endl;
        }
        std::cout << "Trying to acquire the target symbol...";
        void * tmp_ptr = dlsym(handle, target_symbol);
        memcpy(&orig_func, &tmp_ptr, sizeof(&tmp_ptr));
        std::cout << "...done" << std::endl;
        char *error_msg = dlerror();
        if (error_msg != nullptr) {
            std::cout << "Unable to resolve " << target_symbol << " symbol!" << std::endl;
            std::cerr << error_msg << std::endl;
            std::terminate();
        } else {
            std::cout << "Symbol " << target_symbol << " original address:" << &orig_func << std::endl;
        }
        std::cout << "***********************************************" << std::endl;
    }
}

// Function prototype
double move_semantics_test::VectorWithoutMoveSem::computeSum() const
{
    std::chrono::system_clock::time_point start, end;
    // Call of the original function and measurement of execution time
    call_count += 1;
    start = std::chrono::high_resolution_clock::now();
    std::cout << "Call of the original function ...";
    
    double ret_val = (this->*orig_func)();
    
    std::cout << "...done" << std::endl;
    end = std::chrono::high_resolution_clock::now();
    total_time_used += std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    return ret_val;
    
}


//Library finalizer
void __attribute__((destructor)) finalize()
{
    // Printing of the results
    std::cout << "***********************************************" << std::endl;
    std::cout << "RESULTS FOR FUNCTION : " << "computeSum" << std::endl;
    std::cout << "Call count = " << call_count << std::endl;
    std::cout << "Total time consumed = " << total_time_used.count() << " microseconds" << std::endl;
    std::cout << "***********************************************" << std::endl;
}
