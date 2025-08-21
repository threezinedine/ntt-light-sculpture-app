#pragma once

#if defined(_DEBUG)
#define NTT_ASSERT(condition)                                                               \
    if ((condition) == false)                                                               \
    {                                                                                       \
        printf("Assertion failed: %s, file %s, line %d\n", #condition, __FILE__, __LINE__); \
        __debugbreak();                                                                     \
    }
#else
#define NTT_ASSERT(condition)
#endif