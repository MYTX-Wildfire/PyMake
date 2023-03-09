#include <foo/foo.h>
#include <gtest/gtest.h>

TEST(FooTest, FooReturns42)
{
	EXPECT_EQ(42, foo());
}
