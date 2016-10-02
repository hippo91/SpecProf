#include <stdexcept>

template <typename T>
T operator+(const T& v_a, const T& v_b) throw(std::length_error)
{
  if (v_a.size() != v_b.size()) {
    throw std::length_error("Not able to add two vectors of different sizes!");
  }
  T _result(v_a.size(), v_a.getName() + "+" + v_b.getName());
  for (std::size_t i_item(0); i_item < _result.size(); ++i_item) {
    _result[i_item] = v_a[i_item] + v_b[i_item];
  }
  return _result;
}
