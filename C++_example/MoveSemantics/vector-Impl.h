#ifndef MOVE_SEMANTICS_TEST_VECTOR_IMPL_H
#define MOVE_SEMANTICS_TEST_VECTOR_IMPL_H

#include <stdexcept>

template <typename T>
T operator+(const T& v_a, const T& v_b) throw(std::length_error);

#include "vector-Impl.cc"
#endif
