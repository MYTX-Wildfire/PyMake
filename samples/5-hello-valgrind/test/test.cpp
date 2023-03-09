#include <atomic>
#include <chrono>
#include <foo/foo.h>
#include <gtest/gtest.h>
#include <memory>
#include <mutex>
#include <thread>

TEST(FooTest, LeakTest)
{
	// Leak the pointer returned by `foo()` so Valgrind can detect it
	EXPECT_EQ(42, *foo());
}

TEST(FooTest, ThreadTest)
{
	std::atomic_bool stopFlag = false;

	// Start two threads that both touch the same memory address in an unsafe
	//   manner so Helgrind has something to detect
	int i = 42;
	auto threadFunc = [&stopFlag, &i]() {
		while (!stopFlag)
		{
			++i;
		}
	};

	std::thread t1(threadFunc);
	std::thread t2(threadFunc);

	std::this_thread::sleep_for(std::chrono::seconds(1));
	stopFlag = true;
	t1.join();
	t2.join();
}

TEST(FooTest, LockTest)
{
	std::atomic_bool stopFlag = false;
	std::unique_ptr<int> i(new int(0));
	auto threadFunc = [&stopFlag, &i] {
		while (!stopFlag)
		{
			++(*i);
		}
	};

	std::thread t1(threadFunc);
	std::thread t2(threadFunc);

	std::this_thread::sleep_for(std::chrono::seconds(1));
	stopFlag = true;
	t1.join();
	t2.join();
}
