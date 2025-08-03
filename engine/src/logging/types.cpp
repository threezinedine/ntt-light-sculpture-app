#include "engine/logging/types.h"

namespace NTT_NS
{
    string LogLevelToString(LogLevel level)
    {
        switch (level)
        {
        case LogLevel::DEBUG:
            return "DEBUG";
        case LogLevel::INFO:
            return "INFO";
        case LogLevel::WARNING:
            return "WARNING";
        case LogLevel::ERROR:
            return "ERROR";
        case LogLevel::FATAL:
            return "FATAL";
        default:
            return "Unknown";
        }
    }
} // namespace NTT_NS
