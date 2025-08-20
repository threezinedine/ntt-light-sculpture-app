#include "engine/renderer/program.h"
#include "GL/glew.h"
#include <stdexcept>

namespace NTT_NS
{
    void GetShaderNameByType(u32 shaderType, string &outName)
    {
        switch (shaderType)
        {
        case GL_VERTEX_SHADER:
            outName = "Vertex Shader";
            break;
        case GL_FRAGMENT_SHADER:
            outName = "Fragment Shader";
            break;
        case GL_COMPUTE_SHADER:
            outName = "Compute Shader";
            break;
        default:
            outName = "Unknown Shader";
            break;
        }
    }

    u32 MakeShader(u32 shaderType, const char *shaderSource)
    {
        u32 shaderId = glCreateShader(shaderType);
        glShaderSource(shaderId, 1, &shaderSource, nullptr);
        glCompileShader(shaderId);

        // error checking
        int success;

        glGetShaderiv(shaderId, GL_COMPILE_STATUS, &success);
        if (!success)
        {
            char infoLog[512];
            glGetShaderInfoLog(shaderId, 512, nullptr, infoLog);
            throw std::runtime_error("Failed to compile shader: " + string(infoLog));
        }

        return shaderId;
    }

    Program::Program()
        : m_programID(0)
    {
        m_shaderIDs.reserve(MAX_SHADERS_PER_PROGRAM);
    }

    Program::~Program()
    {
        glDeleteProgram(m_programID);
    }

    void Program::Append(u32 shaderID)
    {
        if (m_shaderIDs.size() >= MAX_SHADERS_PER_PROGRAM)
        {
            throw std::runtime_error("Maximum shader limit reached");
        }
        m_shaderIDs.push_back(shaderID);
    }

    void Program::Compile()
    {
        m_programID = glCreateProgram();

        for (const auto &shaderID : m_shaderIDs)
        {
            glAttachShader(m_programID, shaderID);
        }

        glLinkProgram(m_programID);

        for (const auto &shaderID : m_shaderIDs)
        {
            glDeleteShader(shaderID);
        }

        glUseProgram(0);
    }

    void Program::Use()
    {
        glUseProgram(m_programID);
    }
} // namespace NTT_NS