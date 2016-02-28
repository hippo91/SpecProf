// this file is an example of how to intercept a C++ method by using the
// LD_PRELOAD environment variable of the GNU dynamic linker.
//
// it works like this:
//
// 1) define a method that will have the same symbol as the intercepted
//    method when compiled. For example, the method Foo::getValue()
//    defined here has the mangled symbol "_ZNK3Foo8getValueEv".
//    tools like nm, objdump or readelf can display the symbols of
//    binaries.
//
// 2) if you want to call the original method from your new method,
//    you can get a pointer to it with dlsym() and the mangled name.
//
// 3) compile your intercept code into its own shared library,
//    for example with "g++ -g -Wall -shared -fPIC -ldl foo.cpp -o foo.so".
//    "-ldl" should only be necessary if you use dlsym().
//
// 4) set LD_PRELOAD to the path of your new shared library and call the
//    program in which you want to intercept something. in bash, you can
//    do it like this: "LD_PRELOAD=./foo.so /usr/bin/some_program".

#include <string.h>

// necessary for RTLD_NEXT in dlfcn.h
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <dlfcn.h>


class Foo
{
public:
  unsigned int getValue() const;
};

unsigned int Foo::getValue() const
{
  // define the pointer-to-member type
  typedef unsigned int (Foo::*methodType)() const;

  static methodType origMethod = 0;
  if (origMethod == 0)
  {
    // use the mangled method name here. RTLD_NEXT means something like
    // "search this symbol in any libraries loaded after the current one".
    void *tmpPtr = dlsym(RTLD_NEXT, "_ZNK3Foo8getValueEv");

    // not even reinterpret_cast can convert between void* and a method ptr,
    // so i'm doing the worst hack i've ever seen.
    memcpy(&origMethod, &tmpPtr, sizeof(&tmpPtr));
  }

  // here we call the original method
  unsigned int origValue = (this->*origMethod)();

  return 1000 + origValue;
}