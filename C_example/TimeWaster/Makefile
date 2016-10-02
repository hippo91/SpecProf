#-------------------------------------------
# OPTIONS
#-------------------------------------------

# Choice of compilator (g++ by default)
CC=$(CPL)
ifeq ($(CC),)
CC=g++
endif

# Want to compile with debug symbols?
DEBUG=$(DBG)

ifeq ($(DEBUG), true)
CFLAGS_BASE=-O0 -g3 -Wall
else
CFLAGS_BASE=-O3 -Wall -march=native -mtune=native
endif

# Want to use libraries?
ifeq ($(LIBRARY), true)
CFLAGS_LIB=-fPIC
CFLAGS=$(CFLAGS_BASE) $(CFLAGS_LIB)
else
CFLAGS=$(CFLAGS_BASE)
endif

#-------------------------------------------
# RULES
#-------------------------------------------

all: time_waster.exe

usage:
	@echo "-------------------------------------------------------------------------------------------------------------"
	@echo "To compile a fully static executable simply run : 'make'"
	@echo "To compile with a library : 'make LIBRARY=true'"
	@echo "You can ask for debug symbol adding 'DEBUG=true' to the above commands"
	@echo "By default compilator is g++. You can override this settings by "\
	"adding 'CC=your_compilator' to the above commands"
	@echo "-------------------------------------------------------------------------------------------------------------"


TimeWaster.o: TimeWaster.c 
	$(CC) $(CFLAGS) -c $^

# Shared Objects if LIBRARY is true
ifeq ($(LIBRARY), true)
libtimewaster.so: TimeWaster.o
	$(CC) $(CFLAGS) -lm -shared $^ -o libtimewaster.so
endif

# Executable
ifeq ($(LIBRARY), true)
time_waster.exe: Launcher.c libtimewaster.so
	$(CC) $(CFLAGS_BASE) -o time_waster.exe -I . -L. -ltimewaster $<
else
time_waster.exe: Launcher.c TimeWaster.o
	$(CC) $(CFLAGS) $^ -o time_waster.exe
endif

# Cleaning
clean :
	rm -rf *.gch *.o

cleanall : clean
	rm -rf libtimewaster.so time_waster.exe
