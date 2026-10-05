#include "discount.h"

namespace discount {

double apply(double total, int loyalty_years) {
  if (total < 0) {
    throw std::invalid_argument("total must not be negative");
  }
  double rate = 0.0;
  if (loyalty_years >= 10) {
    rate = 0.20;
  } else if (loyalty_years >= 5) {
    rate = 0.10;
  } else if (loyalty_years >= 1) {
    rate = 0.05;
  }
  return total * (1.0 - rate);
}

}  // namespace discount
