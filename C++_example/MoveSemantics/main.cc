#include <iostream>
#include "vector_with_move_sem.h"
#include "test_move_semantics.h"

int main()
{
  std::cout << "Vector creation ..." << std::endl;
  move_semantics_test::VectorWithMoveSem huge_rdm_vector_a(10000000, "my_huge_rdm_vector_a", 0, true);
  move_semantics_test::VectorWithMoveSem huge_rdm_vector_b(10000000, "my_huge_rdm_vector_b", 0, true);
  std::cout << "...done!" << std::endl;
  test_functions::testReturnValueOptimization(huge_rdm_vector_a, huge_rdm_vector_b);
  test_functions::testWithoutMoveCtor(huge_rdm_vector_a, huge_rdm_vector_b);
  test_functions::testWithMoveCtor(huge_rdm_vector_a, huge_rdm_vector_b);
  test_functions::testWithoutMoveOperator(huge_rdm_vector_a, huge_rdm_vector_b);
  test_functions::testWithMoveOperator(huge_rdm_vector_a, huge_rdm_vector_b);
  std::cout << "The sum of vector A is : " << huge_rdm_vector_a.computeSum() << std::endl;
  std::cout << "The sum of vector B is : " << huge_rdm_vector_b.computeSum() << std::endl;
  return 0;
}
