#include "ntt_assertion.h"

::testing::AssertionResult AssertVec3(const Vec3 &actual, const Vec3 &expected)
{
    char errorBuffer[ERROR_BUFFER_SIZE];
    snprintf(errorBuffer, sizeof(errorBuffer), "\n\tExpected: (%.3f, %.3f, %.3f), \n\tActual:   (%.3f, %.3f, %.3f)", expected[0], expected[1], expected[2], actual[0], actual[1], actual[2]);

    for (int i = 0; i < 3; ++i)
    {
        if (expected[i] != actual[i])
        {
            return ::testing::AssertionFailure() << errorBuffer;
        }
    }
    return ::testing::AssertionSuccess();
}