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
        return 0;
    }

    Program::Program()
    {
    }

    Program::Program(string vertexShader, string fragmentShader)
        : m_programID(0), m_vertexShaderSource(vertexShader), m_fragmentShaderSource(fragmentShader)
    {
    }

    Program::~Program()
    {
        glDeleteProgram(m_programID);
    }

    void Program::Compile()
    {
        m_programID = glCreateProgram();

        u32 vertexShaderID = glCreateShader(GL_VERTEX_SHADER);
        CompileShader(vertexShaderID, m_vertexShaderSource.c_str());

        u32 fragmentShaderID = glCreateShader(GL_FRAGMENT_SHADER);
        CompileShader(fragmentShaderID, m_fragmentShaderSource.c_str());

        glLinkProgram(m_programID);
        glDeleteShader(vertexShaderID);
        glDeleteShader(fragmentShaderID);
        glUseProgram(0);
    }

    void Program::CompileShader(u32 shaderID, const char *shaderSource)
    {
        glShaderSource(shaderID, 1, &shaderSource, nullptr);
        glCompileShader(shaderID);

        // error checking
        int success;

        glGetShaderiv(shaderID, GL_COMPILE_STATUS, &success);
        if (!success)
        {
            char infoLog[512];
            glGetShaderInfoLog(shaderID, 512, nullptr, infoLog);
            throw std::runtime_error("Failed to compile shader: " + string(infoLog));
        }

        glAttachShader(m_programID, shaderID);
    }

    void Program::Use()
    {
        glUseProgram(m_programID);
    }
} // namespace NTT_NS