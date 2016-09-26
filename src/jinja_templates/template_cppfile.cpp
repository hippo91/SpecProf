// Mandatory includes
#include <iostream>
#include <string>
#include <exception>
#include <signal.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
// necessary for RTLD_NEXT in dlfcn.h
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <dlfcn.h>

// --------------------------------------------------------------
// -- Optional includes
// --------------------------------------------------------------
{% if opt_includes is not none %}
{% for include in opt_includes %}
#include "{{ include }}"
{% endfor %}
{% endif %}

// --------------------------------------------------------------
// -- GLOBAL VARIABLES
// --------------------------------------------------------------

// Target library path
static const std::string target_library("{{ target_library }}");
// Target symbol
static const std::string target_symbol("{{ target_symbol }}");
// Specific pointer to function type
typedef void (*func_ptr)({{ func_params|safe }});
// Address of the target function will be stored in :
static func_ptr orig_func(nullptr);
// Total number of calls
static long int call_count(0);
// Cumulative cpu time used by the function
static double total_cpu_time_used(0.);
// Cumulative real time used by the function
static double total_real_time_used(0.);

// --------------------------------------------------------------
// -- FUNCTIONS
// --------------------------------------------------------------

//Library Initializer
void __attribute__((constructor)) setup()
{
    if (orig_func == nullptr) {
        std::cout << "--------------------------------" << std::endl;
        std::cout << "Call of the library initializer!" << std::endl;
        void *handle;  // Handle of the target library
        dlerror();  // Cleaning of potential previous error message
        handle = dlopen(target_library, RTLD_LAZY);
        if (!handle) {
            std::cerr << "Unable to access origin library!" << std::endl;
            std::cerr << dlerror() << std::endl;
            std::terminate();
        } else {
            std::cout << "Library " << target_library << " found and opened successfully!" << std::endl;
        }
        orig_func = dlsym(handle, target_symbol);
        char *error_msg = dlerror();
        if (error_msg != nullptr) {
            std::cerr << "Unable to resolve " << target_symbol << " symbol!" << std::endl;
            std::cerr << error_msg << std::endl;
            std::terminate();
        } else {
            std::cout << "Symbol " << target_symbol << " original address: " << orig_func << std::endl;
        }
        std::cout << "--------------------------------" << std::endl;
    }
}

// Function prototype
{{ func_signature|safe }}
{
    clock_t start;
    struct timeval start_r, end_r;
    // Call of the original function and measurement of execution time
    call_count += 1;
    start = clock();
    gettimeofday(&start_r, NULL);
    (*orig_func)({{ func_params_names|safe }});
    gettimeofday(&end_r, NULL);
    total_real_time_used += static_cast<double>(end_r.tv_sec - start_r.tv_sec) * 1e+06 +
                            static_cast<double> (end_r.tv_usec - start_r.tv_usec);
    total_cpu_time_used += static_cast<double> (clock() - start) / CLOCKS_PER_SEC;
}


//Library finalizer
void __attribute__((destructor)) finalize()
{
    // Printing of the results
    std::cout << "--------------------------------" << std::endl;
    std::cout << "Call count = " << call_count << std::endl;
    std::cout << "Cpu time consumed = " << total_cpu_time_used << " seconds" << std::endl;
    std::cout << "Real time consumed = " << total_real_time_used / 1e+06 << " seconds" << std::endl;
    std::cout << "--------------------------------" << std::endl;
}
