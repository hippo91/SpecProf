// Mandatory includes
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <time.h>
#include <sys/time.h>
// necessary for RTLD_NEXT in dlfcn.h
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <dlfcn.h>
{% if opt_includes is not none %}
// Optional includes
{% for include in opt_includes %}
#include "{{ include }}"
{% endfor %}
{% endif %}

// Function prototype
{{ func_signature }}
{
  // Define the target library path
  static const char *target_library = "{{ target_library }}";
  // Define the target symbol
  static const char *target_symbol = "{{ target_symbol }}";
  // Define the specific pointer to function type
  typedef void (*func_ptr)({{ func_params }});
  static func_ptr orig_func = NULL;
  static long int call_count = 0;  // we count the total number of calls
  static double total_cpu_time_used = 0.;  // we measure the cpu time used by the function
  static double total_real_time_used = 0.;  // we measure the real time used by the function 
  clock_t start;
  struct timeval start_r, end_r; 

  // Initialization of wrapper
  if (orig_func == NULL)
  {
    void *handle;  // handle of the target library
    dlerror();  // Cleaning of potential previous error message
    handle = dlopen(target_library, RTLD_LAZY);
    if (!handle) {
      printf("Unable to access origin library!\n");
      fputs (dlerror(), stderr);
      exit(1);
    } else {
      printf("Library %s found and opened successfully!\n", target_library);
    }
    orig_func = dlsym(handle, target_symbol);
    char *error_msg = dlerror();
    if (error_msg != NULL) {
      printf("Unable to resolve %s symbol!\n", target_symbol);
      fputs(error_msg, stderr);
      raise(SIGABRT);
    } else {
      printf("Symbol %s original adress: %p\n", target_symbol, orig_func);
    }
    getchar();
  }
  // Call of the original function and measurement of execution time
  call_count += 1;
  start = clock();
  gettimeofday(&start_r, NULL);
  (*orig_func)({{ func_params_names }});
  gettimeofday(&end_r, NULL);
  total_real_time_used += ((double) (end_r.tv_sec - start_r.tv_sec)) * 1e+06 + ((double) (end_r.tv_usec - start_r.tv_usec));
  total_cpu_time_used += ((double) (clock() - start)) / CLOCKS_PER_SEC;
  // Printing
  printf("Call count = %ld\n", call_count);
  printf("Cpu time consumed = %f seconds\n", total_cpu_time_used);
  printf("Real time consumed = %f seconds\n", total_real_time_used / 1e+06);
}
