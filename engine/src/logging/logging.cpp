#include <chrono>
#include <cstdio>
#include "engine/common/common.h"
#include "engine/logging/logging.h"
#include "engine/singletonManager/singletonManager.h"

namespace NTT_NS
{
    LogCallback Logging::s_logCallback = nullptr;

    void Logging::Log(LogLevel level, const string &message)
    {
        printf("[%s] - %d - %s\n", LogLevelToString(level).c_str(), _get_timestamp(), message.c_str());
        if (s_logCallback != nullptr)
        {
            EngineLogRecord record;
            record.level = level;
            record.message = message;
            record.unixTimestamp = _get_timestamp();
            s_logCallback(record);
        }
    }

    u32 Logging::_get_timestamp()
    {
        auto now = std::chrono::system_clock::now();
        auto now_ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
        return now_ms;
    }

    void Logging::SetLogCallback(LogCallback callback)
    {
        s_logCallback = callback;
    }
} // namespace NTT_NS
