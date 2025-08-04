#pragma once
#include "engine/common/common.h"
#include "types.h"

namespace NTT_NS
{
    /**
     * @brief The structure store all the information of the log message which will be sent to the application.
     */
    struct EngineLogRecord
    {
        LogLevel level;    ///< The information of the important of the message.
        string message;    ///< The main content of the message.
        u32 unixTimestamp; ///< The time when the message is logged.
    };

    /**
     * @brief This callback will be called when the engine want to send a log message to the application.
     *
     * The application should implement the callback (should be the handler in logging) for
     *      handling this message data.
     */
    typedef Function<void, const EngineLogRecord &> LogCallback;

    class Logging
    {
    public:
        /**
         * @brief Main method of the c++ engine logging system, for sending the log message to the application.Log
         *
         * @param level The importance of the message (if the message has the importance less than the current
         *      log system level, it will not be sent to the application).
         * @param message The content of the sent message.
         */
        static void Log(LogLevel level, const string &message) NTT_PYTHON_BINDING;

        /**
         * @brief Configure the python callback for handling the message Record.
         *
         * @note If the python set the callback, it must release the callback when the application is closing.
         *      Otherwise, the application will crash when the engine is shutting down.
         */
        static void SetLogCallback(LogCallback callback) NTT_PYTHON_BINDING;

    private:
        static u32 _get_timestamp();

    private:
        static LogCallback s_logCallback;
    };
} // namespace NTT_NS

#define NTT_LOG_DEBUG(message) ::NTT_NS::Logging::Log(::NTT_NS::LogLevel::DEBUG, message)
#define NTT_LOG_INFO(message) ::NTT_NS::Logging::Log(::NTT_NS::LogLevel::INFO, message)
#define NTT_LOG_WARN(message) ::NTT_NS::Logging::Log(::NTT_NS::LogLevel::WARNING, message)
#define NTT_LOG_ERROR(message) ::NTT_NS::Logging::Log(::NTT_NS::LogLevel::ERROR, message)
#define NTT_LOG_FATAL(message) ::NTT_NS::Logging::Log(::NTT_NS::LogLevel::FATAL, message)