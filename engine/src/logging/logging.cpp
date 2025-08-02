#include "engine/common/common.h"
#include "engine/logging/logging.h"
#include <cstdio>

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
        printf("[INFO] %s\n", message.c_str());
    }

    void Logging::debug(const std::string &message)
    {
        printf("[DEBUG] %s\n", message.c_str());
    }

    void Logging::warning(const std::string &message)
    {
        printf("[WARNING] %s\n", message.c_str());
    }

    void Logging::error(const std::string &message)
    {
        printf("[ERROR] %s\n", message.c_str());
    }
} // namespace NTT_NS
