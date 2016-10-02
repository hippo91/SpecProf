#ifndef TEST_MOVE_SEMANTICS_H
#define TEST_MOVE_SEMANTICS_H

#include "vector_with_move_sem.h"

namespace test_functions {

void testReturnValueOptimization(const move_semantics_test::VectorWithMoveSem& vec_a,
                                 const move_semantics_test::VectorWithMoveSem& vec_b);

void testWithoutMoveCtor(const move_semantics_test::VectorWithMoveSem& vec_a,
                         const move_semantics_test::VectorWithMoveSem& vec_b);

void testWithMoveCtor(const move_semantics_test::VectorWithMoveSem& vec_a,
                      const move_semantics_test::VectorWithMoveSem& vec_b);

void testWithoutMoveOperator(const move_semantics_test::VectorWithMoveSem& vec_a,
                             const move_semantics_test::VectorWithMoveSem& vec_b);

void testWithMoveOperator(const move_semantics_test::VectorWithMoveSem& vec_a,
                          const move_semantics_test::VectorWithMoveSem& vec_b);

}

#endif
