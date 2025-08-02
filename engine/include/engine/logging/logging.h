#pragma once
#include "engine/common/common.h"
#include <string>

namespace NTT_NS
{
    class Logging
    {
    public:
        Logging();
        ~Logging();

        void info(const std::string &message);
        void debug(const std::string &message);
        void warning(const std::string &message);
        void error(const std::string &message);

    private:
        std::string _get_log_message(const std::string &message, const std::string &level);
        std::string _get_timestamp();
    };
} // namespace NTT_NS
