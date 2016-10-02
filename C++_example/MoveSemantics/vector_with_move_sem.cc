#include "vector_with_move_sem.h"
#include <sstream>
#include <random>
#include <iostream>
#include <iomanip>
/*-------------------------------------*/

namespace move_semantics_test {

  //Minimal ctor
  VectorWithMoveSem::
  VectorWithMoveSem(const std::string& name) : base_t(name)
  {
  }

  // Usual ctor
  VectorWithMoveSem::
  VectorWithMoveSem(const int& size, const std::string& name, const double& default_value, bool randomized)
      : base_t(size, name, default_value, randomized)
  {
  }

//Copy ctor
  VectorWithMoveSem::
  VectorWithMoveSem(const VectorWithMoveSem& origin): base_t(origin)
  {
  }

  // Move ctor
  VectorWithMoveSem::
  VectorWithMoveSem(VectorWithMoveSem&& origin)
  {
    dynamic_cast<std::vector<double>&>(*this) = std::move(origin);
    m_name = std::move(origin.m_name + "_move");
    std::cout << "Use of move ctor for " << m_name << "!" << std::endl;
    origin.m_name = "";
    if (origin.size() != 0) {
      std::cerr << "Move ctor failed! origin's size is not nil!" << std::endl;
    }
  }

  // Copy op
  VectorWithMoveSem& VectorWithMoveSem::
  operator=(const VectorWithMoveSem& origin)
  {
    std::cout << "Use of copy operator!" << std::endl;
    dynamic_cast<base_t&>(*this) = base_t::operator=(origin);
    m_name = origin.m_name + "_copy";
    return *this;
  }

  // Move op
  VectorWithMoveSem& VectorWithMoveSem::
  operator=(VectorWithMoveSem&& origin)
  {
    std::cout << "Use of move operator!" << std::endl;
    dynamic_cast<std::vector<double>&>(*this) = std::vector<double>::operator=(std::move(origin));
    m_name = origin.m_name + "_copy";
    origin.m_name = "";
    if (origin.size() != 0) {
      std::cerr << "Move operator failed! origin's size is not nil!" << std::endl;
    }
    return *this;
  }

}  // namespace move_semantics_test
