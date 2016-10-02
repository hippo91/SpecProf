#ifndef MOVE_SEMANTICS_TEST_VECTOR_WITH_MOVE_SEM_H
#define MOVE_SEMANTICS_TEST_VECTOR_WITH_MOVE_SEM_H

/*-------------------------------------*/
#include <vector>
#include <ostream>
#include <string>
#include <stdexcept>
#include "vector_without_move_sem.h"
/*-------------------------------------*/

namespace move_semantics_test {

  class VectorWithMoveSem : public VectorWithoutMoveSem
  {

    typedef VectorWithoutMoveSem base_t;

  public:
    //Default dtor
    ~VectorWithMoveSem() {};

    //Minimal ctor
    explicit VectorWithMoveSem(const std::string& name);

    // Usual ctor
    VectorWithMoveSem(const int& size, const std::string& name, const double& default_value=0., bool randomized=false);

    // Copy ctor
    VectorWithMoveSem(const VectorWithMoveSem& origin);

    // Move ctor
    VectorWithMoveSem(VectorWithMoveSem&& origin);

    // Copy op
    VectorWithMoveSem& operator=(const VectorWithMoveSem& origin);

    // Move op
    VectorWithMoveSem& operator=(VectorWithMoveSem&& origin);
  };

}  // namespace move_semantics_test

#endif
