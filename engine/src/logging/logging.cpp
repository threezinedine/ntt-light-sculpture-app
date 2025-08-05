#include <chrono>
#include <cstdio>
#include "engine/common/common.h"
#include "engine/logging/logging.h"
#include "engine/singletonManager/singletonManager.h"

namespace NTT_NS
{
    NTT_DEFINE_SINGLETON(Logging);

    Logging::Logging()
        : m_logCallback(nullptr)
    {
    }

    Logging::~Logging()
    {
        m_logCallback = nullptr;
    }

    void Logging::Log(LogLevel level, const string &message)
    {
        if (m_logCallback != nullptr)
        {
            EngineLogRecord record;
            record.level = level;
            record.message = message;
            record.unixTimestamp = _get_timestamp();
            m_logCallback(record);
        }
    }

    u32 Logging::_get_timestamp()
    {
        auto now = std::chrono::system_clock::now();
        auto now_ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
        return now_ms;
    }
} // namespace NTT_NS
