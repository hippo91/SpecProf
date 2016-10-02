#include "vector_without_move_sem.h"
#include <sstream>
#include <random>
#include <iostream>
#include <iomanip>
/*-------------------------------------*/

namespace move_semantics_test {

  // Default ctor
  VectorWithoutMoveSem::
  VectorWithoutMoveSem() : base_t(), m_name(std::string())
  {
  }

  // Minimal ctor
  VectorWithoutMoveSem::
  VectorWithoutMoveSem(const std::string& name) : base_t(), m_name(name)
  {
    std::cout << "Use of minimal VectorWithoutMoveSem ctor for " << m_name << "!" << std::endl;
  }

  // Usual ctor
  VectorWithoutMoveSem::
  VectorWithoutMoveSem(const int& size, const std::string& name, const double& default_value, bool randomized)
      : base_t(static_cast<std::size_t>(size), default_value), m_name(name)
  {
    std::cout << "Use of usual VectorWithoutMoveSem ctor for " << m_name << "!" << std::endl;
    if (randomized) {
      std::random_device rd;
      std::mt19937 gen(rd());
      std::uniform_real_distribution<> dis(-1000, 1000);
      for (auto it(this->begin()); it < this->end(); ++it) {
        *it = dis(gen);
      }
    }
  }

  // Copy ctor
  VectorWithoutMoveSem::
  VectorWithoutMoveSem(const VectorWithoutMoveSem& origin): base_t(origin), m_name(origin.m_name + "_copy")
  {
    std::cout << "Use of VectorWithoutMoveSem copy ctor for " << m_name << "!" << std::endl;
  }

  // Copy op
  VectorWithoutMoveSem& VectorWithoutMoveSem::
  operator=(const VectorWithoutMoveSem& origin)
  {
    std::cout << "Use of VectorWithoutMoveSem copy operator!" << std::endl;
    dynamic_cast<base_t&>(*this) = base_t::operator=(origin);
    m_name = origin.m_name + "_copy";
    return *this;
  }

  // Name getter
  std::string VectorWithoutMoveSem::
  getName()
  {
    return m_name;
  }

  // Name getter for const
  std::string VectorWithoutMoveSem::
  getName() const
  {
    return m_name;
  }

  // Compute sum of all components
  double VectorWithoutMoveSem::
  computeSum() const
  {
    double sum{0};
    for (auto _it(this->begin()); _it < this->end(); ++_it) {
      sum += *_it;
    }
    return sum;
  }
}  // namespace move_semantics_test

std::ostream& operator<<(std::ostream& stream, const move_semantics_test::VectorWithoutMoveSem& v)
{
  size_t max_print_size(20), trailing_size(3), _v_size(v.size());
  stream << v.getName() << " : [";
  if (_v_size < max_print_size) {
    for (size_t i_item(0); i_item < _v_size - 1; ++i_item) {
      stream << v[i_item] << ", ";
    }
    stream << v[_v_size - 1] << "]";
  } else {
    std::ostringstream right_buffer;
    for (size_t i_item(0); i_item < trailing_size; ++i_item) {
      stream << v[i_item] << ", ";
      if (i_item != trailing_size - 1) {
        right_buffer << v[_v_size - trailing_size - 1 + i_item] << ", ";
      } else {
        right_buffer << v[i_item] << "]";
      }
    }
    stream << " ... " << right_buffer.str();
  }
  stream << " -> size : " << _v_size;
  return stream;
}
