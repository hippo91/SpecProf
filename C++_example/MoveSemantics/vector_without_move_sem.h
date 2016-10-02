#ifndef MOVE_SEMANTICS_TEST_VECTOR_WITHOUT_MOVE_SEM_H
#define MOVE_SEMANTICS_TEST_VECTOR_WITHOUT_MOVE_SEM_H

/*-------------------------------------*/
#include <vector>
#include <ostream>
#include <string>
/*-------------------------------------*/

namespace move_semantics_test {

  class VectorWithoutMoveSem : public std::vector<double>
  {
  protected:
    typedef std::vector<double> base_t;
    std::string m_name;

  public:
    // Default ctor
    VectorWithoutMoveSem();

    // Default dtor
    ~VectorWithoutMoveSem() {};

    // Minimal ctor
    explicit VectorWithoutMoveSem(const std::string& name);

    // Usual ctor
    VectorWithoutMoveSem(const int& size, const std::string& name, const double& default_value=0., bool randomized=false);

    // Copy ctor
    VectorWithoutMoveSem(const VectorWithoutMoveSem& origin);

    // Copy op
    VectorWithoutMoveSem& operator=(const VectorWithoutMoveSem& origin);

    // Name getter
    virtual std::string getName();

    // Name getter for const
    virtual std::string getName() const;

    // Sum of all the components
    virtual double computeSum() const;
  };

}  // namespace move_semantics_test

std::ostream& operator<<(std::ostream& stream, const move_semantics_test::VectorWithoutMoveSem& v);

#endif
