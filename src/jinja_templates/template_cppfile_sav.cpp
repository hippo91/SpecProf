// Mandatory includes
#include <iostream>
#include <string>
#include <exception>
#include <chrono>
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
// Cumulative time used by the function
static std::chrono::microseconds total_time_used;

// --------------------------------------------------------------
// -- FUNCTIONS
// -------------------------------------------------------------

//Library Initializer
void __attribute__((constructor)) setup()
{
    if (orig_func == nullptr) {
        std::cout << "--------------------------------" << std::endl;
        std::cout << "Call of the library initializer!" << std::endl;
        void *handle;  // Handle of the target library
        dlerror();  // Cleaning of potential previous error message
        std::cout << "Trying to open the target library..." << std::endl;
        handle = dlopen(target_library.c_str(), RTLD_LAZY);
        std::cout << "...done!" << std::endl;
        if (!handle) {
            std::cerr << "Unable to access origin library!" << std::endl;
            std::cerr << dlerror() << std::endl;
            std::terminate();
        } else {
            std::cout << "Library " << target_library << " found and opened successfully!" << std::endl << std::flush;
        }
        std::cout << "Trying to acquire the target symbol..." << std::endl << std::flush;
        orig_func = dlsym(handle, target_symbol.c_str());
        std::cout << "...done" << std::endl;
        char *error_msg = dlerror();
        if (!error_msg) {
            std::cout << "Symbol " << target_symbol << " original address: " << orig_func << std::endl;
        } else {
            std::cerr << error_msg << std::endl;
            std::cerr << "Unable to resolve " << target_symbol << " symbol!" << std::endl;
            std::terminate();
        }
        std::cout << "--------------------------------" << std::endl;
    }
}

// Function prototype
{{ func_signature|safe }}
{
    std::chrono::system_clock::time_point start, end;
    // Call of the original function and measurement of execution time
    call_count += 1;
    start = std::chrono::high_resolution_clock::now();
    (*orig_func)({{ func_params_names|safe }});
    end = std::chrono::high_resolution_clock::now();
    total_time_used += std::chrono::duration_cast<std::chrono::microseconds>(end - start);
}


//Library finalizer
void __attribute__((destructor)) finalize()
{
    // Printing of the results
    std::cout << "--------------------------------" << std::endl;
    std::cout << "RESULTS FOR FUNCTION : " << "{{ func_name }}" << std::endl;
    std::cout << "Call count = " << call_count << std::endl;
    std::cout << "Total time consumed = " << total_time_used.count() << " microseconds" << std::endl;
    std::cout << "--------------------------------" << std::endl;
}
