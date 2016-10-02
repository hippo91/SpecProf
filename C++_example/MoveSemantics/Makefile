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
CFLAGS_BASE=-O0 -g3 -Wall -std=c++14
else
CFLAGS_BASE=-O3 -Wall -march=native -mtune=native -std=c++14
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

all: move_semantics_test.exe

usage:
	@echo "-------------------------------------------------------------------------------------------------------------"
	@echo "To compile a fully static executable simply run : 'make'"
	@echo "To compile with libraries for vectors and tests run : 'make LIBRARY=true'"
	@echo "You can ask for debug symbol adding 'DEBUG=true' to the above commands"
	@echo "By default compilator is g++. You can override this settings by "\
	"adding 'CC=your_compilator' to the above commands"
	@echo "-------------------------------------------------------------------------------------------------------------"

vector_without_move_sem.o: vector_without_move_sem.cc
	$(CC) $(CFLAGS) -c $^

vector_with_move_sem.o: vector_with_move_sem.cc
	$(CC) $(CFLAGS) -c $^

vector-Impl.o: vector-Impl.cc
	$(CC) $(CFLAGS) -c $^

test_move_semantics.o: test_move_semantics.cc
	$(CC) $(CFLAGS) -c $^

# Shared Objects if LIBRARY is true
ifeq ($(LIBRARY), true)
libvector.so: vector_without_move_sem.o vector_with_move_sem.o vector-Impl.o
	$(CC) $(CFLAGS) -lm -shared $^ -o libvector.so

libtest_move_semantics.so: test_move_semantics.o
	$(CC) $(CFLAGS) -lm -shared $^ -o libtest_move_semantics.so
endif

# Executable
ifeq ($(LIBRARY), true)
move_semantics_test.exe: main.cc libvector.so libtest_move_semantics.so
	$(CC) $(CFLAGS_BASE) -o move_semantics_test.exe -I . -L. -lvector -ltest_move_semantics $<
else
move_semantics_test.exe: main.cc test_move_semantics.o vector-Impl.o vector_with_move_sem.o vector_without_move_sem.o
	$(CC) $(CFLAGS) $^ -o move_semantics_test.exe
endif

# Cleaning
clean :
	rm -rf *.gch *.o

cleanall : clean
	rm -rf libvector.so libtest_move_semantics.so move_semantics_test.exe
