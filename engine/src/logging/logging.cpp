#include <chrono>
#include <cstdio>
#include "engine/common/common.h"
#include "engine/logging/logging.h"

namespace NTT_NS
{
    Logging::Logging()
    {
    }

    Logging::~Logging()
    {
    }

    void Logging::info(const std::string &message)
    {
        printf("%s\n", _get_log_message(message, "INFO").c_str());
    }

    void Logging::debug(const std::string &message)
    {
        printf("%s\n", _get_log_message(message, "DEBUG").c_str());
    }

    void Logging::warning(const std::string &message)
    {
        printf("%s\n", _get_log_message(message, "WARNING").c_str());
    }

    void Logging::error(const std::string &message)
    {
        printf("%s\n", _get_log_message(message, "ERROR").c_str());
    }

    std::string Logging::_get_log_message(const std::string &message, const std::string &level)
    {
        char logMessage[1024];
        snprintf(logMessage, sizeof(logMessage),
                 "[%s] - %s - %s", level.c_str(),
                 _get_timestamp().c_str(),
                 message.c_str());
        return std::string(logMessage);
    }

    std::string Logging::_get_timestamp()
    {
        auto now = std::chrono::system_clock::now();
        auto now_ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
        return std::to_string(now_ms);
    }
} // namespace NTT_NS
