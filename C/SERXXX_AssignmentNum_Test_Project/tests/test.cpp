// t/test.cpp
#include "CppUTest/TestHarness.h"
#include "include.h"

TEST_GROUP(tests)
{
};

TEST(tests, FirstTest)
{
  int x = main_stuff();
  CHECK_EQUAL(0, x);
}
