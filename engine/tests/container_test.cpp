#include "ntt_assertion.h"
#include "engine/container/container.h"

using namespace NTT_NS;
using namespace testing;

class TestObject
{
public:
    static u32 instanceCount;

    TestObject(u32 value = 3) : testValue(value)
    {
        TestObject::instanceCount++;
    }

    ~TestObject()
    {
        TestObject::instanceCount--;
    }

    inline u32 getValue() const { return testValue; }

private:
    u32 testValue = 0; // Example member variable
};

u32 TestObject::instanceCount = 0;

#define ASSERT_TEST_OBJECT_COUNT(expected) \
    EXPECT_THAT(TestObject::instanceCount, Eq(expected));

ContainerAllocator<TestObject> allocator = [](void *data = nullptr) -> TestObject *
{
    if (data != nullptr)
    {
        return new TestObject(*static_cast<u32 *>(data));
    }

    return new TestObject();
};

ContainerDeallocator<TestObject> deallocator = [](TestObject *obj)
{
    delete obj;
};

TEST(AllocatorTest, AutoDeleteAllCreatedObject)
{
    {
        Container<TestObject> container(allocator, deallocator);

        container.Create();

        ASSERT_TEST_OBJECT_COUNT(1);
    }

    ASSERT_TEST_OBJECT_COUNT(0);
}

TEST(AllocatorTest, CreateMultipleObjects)
{
    {
        Container<TestObject> container(allocator, deallocator);

        container.Create();
        container.Create();
        container.Create();

        ASSERT_TEST_OBJECT_COUNT(3);
    }

    ASSERT_TEST_OBJECT_COUNT(0);
}

TEST(AllocatorTest, CreateAndDeleteObjects)
{
    {
        Container<TestObject> container(allocator, deallocator);

        container.Create();
        u32 id = container.Create();
        container.Create();

        ASSERT_TEST_OBJECT_COUNT(3);

        container.Destroy(id);

        ASSERT_TEST_OBJECT_COUNT(2);
    }

    ASSERT_TEST_OBJECT_COUNT(0);
}

TEST(AllocatorTest, DeleteNonExistentObject)
{
    {
        Container<TestObject> container(allocator, deallocator);

        container.Create();
        container.Create();
        container.Create();

        ASSERT_TEST_OBJECT_COUNT(3);

        EXPECT_THROW(container.Destroy(100), std::out_of_range); // Attempt to delete an object that does not exist
    }

    ASSERT_TEST_OBJECT_COUNT(0);
}

TEST(AllocatorTest, CheckingIsValidId)
{
    {
        Container<TestObject> container(allocator, deallocator);

        u32 id1 = container.Create();
        u32 id2 = container.Create();
        u32 id3 = container.Create();

        EXPECT_TRUE(container.IsValidId(id1));
        EXPECT_TRUE(container.IsValidId(id2));
        EXPECT_TRUE(container.IsValidId(id3));

        EXPECT_FALSE(container.IsValidId(100)); // Check an ID that does not exist
    }

    ASSERT_TEST_OBJECT_COUNT(0);
}

TEST(AllocatorTest, CheckingIsValidForDeletedObject)
{
    {
        Container<TestObject> container(allocator, deallocator);

        u32 id1 = container.Create();
        u32 id2 = container.Create();
        u32 id3 = container.Create();
        container.Destroy(id2);

        EXPECT_FALSE(container.IsValidId(id2)); // Check an ID that has been deleted
    }

    ASSERT_TEST_OBJECT_COUNT(0);
}

TEST(AllocatorTest, CreateObjectWillUsedDeletedObjectId)
{
    {
        Container<TestObject> container(allocator, deallocator);

        u32 id1 = container.Create();
        container.Destroy(id1);
        u32 id2 = container.Create();

        EXPECT_THAT(id2, Eq(id1)); // Check if the new ID is the same as the deleted ID
    }

    ASSERT_TEST_OBJECT_COUNT(0);
}

TEST(AllocatorTest, CreateObjectWillUsedDeletedObjectIdMultipleTimes)
{
    {
        Container<TestObject> container(allocator, deallocator);

        u32 id1 = container.Create();
        u32 id2 = container.Create();
        u32 id3 = container.Create();
        u32 id4 = container.Create();

        container.Destroy(id3);
        container.Destroy(id1);

        u32 id5 = container.Create();

        EXPECT_THAT(id5, Eq(id1)); // Check if the new ID is the same as the deleted ID
    }

    ASSERT_TEST_OBJECT_COUNT(0);
}

TEST(AllocatorTest, CreateObjectWithData)
{
    {
        Container<TestObject> container(allocator, deallocator);

        u32 data = 42;
        u32 id = container.Create(&data);

        TestObject *obj = container.Get(id);
        EXPECT_THAT(obj->getValue(), Eq(42)); // Assuming TestObject has a method getValue() to retrieve the value
    }

    ASSERT_TEST_OBJECT_COUNT(0);
}

TEST(AllocatorTest, ReachMaxObjectCount)
{
    {
        Container<TestObject> container(allocator, deallocator);

        for (u32 i = 0; i < MAX_CONTAINER_OBJECTS; ++i)
        {
            container.Create();
        }

        EXPECT_THAT(container.Create(), Eq(INVALID_ID));

        EXPECT_THAT(TestObject::instanceCount, Eq(MAX_CONTAINER_OBJECTS));
    }

    ASSERT_TEST_OBJECT_COUNT(0);
}