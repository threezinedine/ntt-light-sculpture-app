#include <chrono>
#include <cstdio>
#include "engine/common/common.h"
#include "engine/logging/logging.h"
#include "engine/singletonManager/singletonManager.h"

namespace NTT_NS
{
    void Logging::Log(LogLevel level, const string &message)
    {
        printf("[%s] - %s - %s\n", LogLevelToString(level).c_str(), _get_timestamp().c_str(), message.c_str());
    }

    string Logging::_get_timestamp()
    {
        auto now = std::chrono::system_clock::now();
        auto now_ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
        return std::to_string(now_ms);
    }
} // namespace NTT_NS
