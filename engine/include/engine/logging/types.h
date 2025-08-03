#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    /**
     * @brief List of all possible level of logging system inside the engine.
     *
     * @note The order of the enum is important. The higher the enum value, the more important the log level is.
     * @note This enum is shared between python and c++ logging system.
     */
    enum class LogLevel
    {
        DEBUG,   ///< Debug level log.
        INFO,    ///< Info level log.
        WARNING, ///< Warning level log.
        ERROR,   ///< Error level log.
        FATAL,   ///< Fatal level log.
    };

    /**
     * @brief Used for converting the log level to the string representation.
     */
    string LogLevelToString(LogLevel level);
} // namespace NTT_NS
