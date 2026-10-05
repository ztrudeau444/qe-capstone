#pragma once
#include <stdexcept>

// The same worked example as the Java, C# and Python profiles, so you can read
// one against another. See Appendix B for the SOLID version of this code.
namespace discount {

// Percentage discount for an order total, by customer tier.
// Throws std::invalid_argument on a negative total.
double apply(double total, int loyalty_years);

}  // namespace discount
