// Week 1: unit tests, including one invalid-input case and one boundary case.
// Note what is NOT here — nothing touches a database, a file or the network.
// That is what makes these unit tests rather than slow integration tests.
#include "../../../../src/cpp/discount.h"
#include "qe_test.h"

QE_TEST(no_discount_below_one_year) {
  QE_ASSERT_EQ(discount::apply(100.0, 0), 100.0);
}

QE_TEST(five_percent_from_one_year) {
  QE_ASSERT_EQ(discount::apply(100.0, 1), 95.0);
}

// Boundaries are where the off-by-one lives. Test the value on each side of
// every threshold, not a value comfortably inside the range.
QE_TEST(boundary_at_five_years) {
  QE_ASSERT_EQ(discount::apply(100.0, 4), 95.0);
  QE_ASSERT_EQ(discount::apply(100.0, 5), 90.0);
}

QE_TEST(boundary_at_ten_years) {
  QE_ASSERT_EQ(discount::apply(100.0, 9), 90.0);
  QE_ASSERT_EQ(discount::apply(100.0, 10), 80.0);
}

QE_TEST(rejects_negative_total) {
  bool threw = false;
  try {
    discount::apply(-1.0, 3);
  } catch (const std::invalid_argument&) {
    threw = true;
  }
  QE_ASSERT(threw);
}

QE_MAIN()
