#include "ntt_assertion.h"

::testing::AssertionResult AssertVec3(const Vec3 &actual, const Vec3 &expected)
{
    char errorBuffer[ERROR_BUFFER_SIZE];
    snprintf(errorBuffer, sizeof(errorBuffer), "\n\tExpected: (%.3f, %.3f, %.3f), \n\tActual:   (%.3f, %.3f, %.3f)", expected.x(), expected.y(), expected.z(), actual.x(), actual.y(), actual.z());

    if (expected.x() != actual.x())
    {
        return ::testing::AssertionFailure() << errorBuffer;
    }
    if (expected.y() != actual.y())
    {
        return ::testing::AssertionFailure() << errorBuffer;
    }
    if (expected.z() != actual.z())
    {
        return ::testing::AssertionFailure() << errorBuffer;
    }
    return ::testing::AssertionSuccess();
}