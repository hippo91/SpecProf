#include <stdio.h>
#include "TimeWaster.h"

int main()
{
	int MAX_COUNT = 10;
	int lt = 1, count=0;
	while (count++ < MAX_COUNT) {
		printf("Count %d : launching the useless loss of time...\n", count);
		waste_time(lt);
		printf("We have lost %d seconds\n", lt);
	}
	return(0);
}
