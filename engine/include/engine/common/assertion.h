#pragma once

#define NTT_ASSERT(condition) \
    if ((condition) == false) \
    {                         \
        __debugbreak();       \
    }