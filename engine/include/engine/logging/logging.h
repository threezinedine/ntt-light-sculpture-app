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
    };
} // namespace NTT_NS
