#include "test_move_semantics.h"
#include <sys/time.h>
#include <iostream>
#include "vector_without_move_sem.h"
#include "vector-Impl.h"
/*-------------------------------------------------------------------------*/
/* Test of the return value optimization                                   */
/*-------------------------------------------------------------------------*/

namespace test_functions {

void testReturnValueOptimization(const move_semantics_test::VectorWithMoveSem& vec_a,
                                 const move_semantics_test::VectorWithMoveSem& vec_b)
{
  struct timeval tv[2];
  gettimeofday (&tv[0], NULL);
  move_semantics_test::VectorWithMoveSem sum_with_rvo(vec_a + vec_b);
  gettimeofday (&tv[1], NULL);
  long int duration = (tv[1].tv_sec * 1e+06 + tv[1].tv_usec - tv[0].tv_sec * 1e+06 - tv[0].tv_usec);
  std::cout << "-------------------------------------------------------------------------------" << std::endl;
  std::cout << "With rvo : it tooks " <<  duration / 1e+06  << " seconds" << std::endl;
  std::cout << "-------------------------------------------------------------------------------" << std::endl;
}

/*-------------------------------------------------------------------------*/
/* Test of the copy constructor because VectorWithoutMoveSem doesn't       */
/* provide a move ctor                                                     */
/*-------------------------------------------------------------------------*/
void testWithoutMoveCtor(const move_semantics_test::VectorWithMoveSem& vec_a,
                         const move_semantics_test::VectorWithMoveSem& vec_b)
{
  struct timeval tv[2];
  gettimeofday (&tv[0], NULL);
  move_semantics_test::VectorWithoutMoveSem sum_without_mv(std::move(vec_a + vec_b));
  gettimeofday (&tv[1], NULL);
  long int duration = (tv[1].tv_sec * 1e+06 + tv[1].tv_usec - tv[0].tv_sec * 1e+06 - tv[0].tv_usec);
  std::cout << "-------------------------------------------------------------------------------" << std::endl;
  std::cout << "Without move ctor : it tooks " <<  duration / 1e+06  << " seconds" << std::endl;
  std::cout << "-------------------------------------------------------------------------------" << std::endl;

}

/*-------------------------------------------------------------------------*/
/* Test of the move constructor because VectorWithMoveSem                  */
/*   provides a move ctor                                                  */
/*-------------------------------------------------------------------------*/
void testWithMoveCtor(const move_semantics_test::VectorWithMoveSem& vec_a,
                      const move_semantics_test::VectorWithMoveSem& vec_b)
{
  struct timeval tv[2];
  gettimeofday (&tv[0], NULL);
  move_semantics_test::VectorWithMoveSem sum_with_mv(std::move(vec_a + vec_b));
  gettimeofday (&tv[1], NULL);
  long int duration = (tv[1].tv_sec * 1e+06 + tv[1].tv_usec - tv[0].tv_sec * 1e+06 - tv[0].tv_usec);
  std::cout << "-------------------------------------------------------------------------------" << std::endl;
  std::cout << "With move ctor : it tooks " <<  duration / 1e+06  << " seconds" << std::endl;
  std::cout << "-------------------------------------------------------------------------------" << std::endl;
}

/*-------------------------------------------------------------------------*/
/* Test of the copy operator because VectorWithoutMoveSem                  */
/* doesn't provide a move operator                                         */
/*-------------------------------------------------------------------------*/
void testWithoutMoveOperator(const move_semantics_test::VectorWithMoveSem& vec_a,
                             const move_semantics_test::VectorWithMoveSem& vec_b)
{
  move_semantics_test::VectorWithoutMoveSem sum_without_move_op(0, "sum_without_move_op");
  struct timeval tv[2];
  gettimeofday (&tv[0], NULL);
  sum_without_move_op = std::move(vec_a + vec_b);
  gettimeofday (&tv[1], NULL);
  long int duration = (tv[1].tv_sec * 1e+06 + tv[1].tv_usec - tv[0].tv_sec * 1e+06 - tv[0].tv_usec);
  std::cout << "-------------------------------------------------------------------------------" << std::endl;
  std::cout << "Without move operator : it tooks " <<  duration / 1e+06  << " seconds" << std::endl;
  std::cout << "-------------------------------------------------------------------------------" << std::endl;
}

/*-------------------------------------------------------------------------*/
/* Test of the move operator because VectorWithMoveSem                     */
/* provides a move operator                                                */
/*-------------------------------------------------------------------------*/
void testWithMoveOperator(const move_semantics_test::VectorWithMoveSem& vec_a,
                          const move_semantics_test::VectorWithMoveSem& vec_b)
{
  move_semantics_test::VectorWithMoveSem sum_with_move_op(0, "sum_with_move_op");
  struct timeval tv[2];
  gettimeofday (&tv[0], NULL);
  sum_with_move_op = std::move(vec_a + vec_b);
  gettimeofday (&tv[1], NULL);
  long int duration = (tv[1].tv_sec * 1e+06 + tv[1].tv_usec - tv[0].tv_sec * 1e+06 - tv[0].tv_usec);
  std::cout << "-------------------------------------------------------------------------------" << std::endl;
  std::cout << "With move operator : it tooks " <<  duration / 1e+06  << " seconds" << std::endl;
  std::cout << "-------------------------------------------------------------------------------" << std::endl;
}

}
