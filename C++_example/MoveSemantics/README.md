# move-semantics-tst
A small c++ app to test the move semantics utility.
This app measure execution time of a simple addition between vectors of two different types.
One implements move semantics (ctor and =) while the other doesn't.
The faster operation is the one for vectors with move semantics.

# Buidling the app
Simply run 'make' to buid the executable. 
For more options run 'make usage'

# Running the app
Run : ./move_semantics_test.exe

# Pre - Requisites
Need of a c++ compilator which handles C++ 2011.

