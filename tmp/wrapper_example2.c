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

// Optional includes
#include "/home/guillaume2/Documents/Informatique/WORKSPACE_ECLIPSE/nonlinear_solver/Newton/miegruneisen.h"

// --------------------------------------------------------------
// -- GLOBAL VARIABLES
// --------------------------------------------------------------

// Target library path
static const char *target_library = "/home/guillaume2/Documents/Informatique/WORKSPACE_ECLIPSE/XVOF_NP/xvof/element/vnr_internal_energy_evolution.so";
// Target symbol
static const char *target_symbol = "solveVolumeEnergy";
// Specific pointer to function type
typedef void (*func_ptr)(MieGruneisenParameters_t *params, const double specific_volume, const double internal_energy,
		double* pressure, double* gamma_per_vol, double* c_son);
// Address of the target function will be stored in :
static func_ptr orig_func = NULL;
// Total number of calls
static long int call_count = 0;
// Cumulative cpu time used by the function
static double total_cpu_time_used = 0.;
// Cumulative real time used by the function
static double total_real_time_used = 0.;

// --------------------------------------------------------------
// -- FUNCTIONS
// --------------------------------------------------------------

//Library Initializer
void __attribute__((constructor)) setup()
{
	if (orig_func == NULL) {
		printf("--------------------------------\n");
		printf("Call of the library initializer!\n");
		void *handle;  // Handle of the target library
		dlerror();  // Cleaning of potential previous error message
		handle = dlopen(target_library, RTLD_LAZY);
		if (!handle) {
			printf("Unable to access origin library!\n");
			fputs(dlerror(), stderr);
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
			printf("Symbol %s original address: %p\n", target_symbol, orig_func);
		}
		printf("--------------------------------\n");
	}
}

// Function prototype
void solveVolumeEnergy(MieGruneisenParameters_t *params, const double specific_volume, const double internal_energy,
		double* pressure, double* gamma_per_vol, double* c_son)
{
	clock_t start;
	struct timeval start_r, end_r;
	// Call of the original function and measurement of execution time
	call_count += 1;
	start = clock();
	gettimeofday(&start_r, NULL);
	(*orig_func)(params, specific_volume, internal_energy, pressure, gamma_per_vol, c_son);
	gettimeofday(&end_r, NULL);
	total_real_time_used += ((double) (end_r.tv_sec - start_r.tv_sec)) * 1e+06 + ((double) (end_r.tv_usec - start_r.tv_usec));
	total_cpu_time_used += ((double) (clock() - start)) / CLOCKS_PER_SEC;
}


//Library finalizer
void __attribute__((destructor)) finalize()
{
	// Printing of the results
	printf("--------------------------------\n");
	printf("Call count = %ld\n", call_count);
	printf("Cpu time consumed = %f seconds\n", total_cpu_time_used);
	printf("Real time consumed = %f seconds\n", total_real_time_used / 1e+06);
	printf("--------------------------------\n");
}
