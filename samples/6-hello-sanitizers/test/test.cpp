#include <foo/foo.h>
#include <gtest/gtest.h>

TEST(FooTest, PastEndArrayAccess)
{
	EXPECT_EQ(42, foo()[1]);
}

TEST(FooTest, MemoryLeak)
{
	EXPECT_EQ(42, *foo());
}
