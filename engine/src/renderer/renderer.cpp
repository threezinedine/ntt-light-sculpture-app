#include <GL/glew.h>
#include <glfw/glfw3.h>
#include <cstdio>
#include <stdexcept>
#include "engine/renderer/renderer.h"
#include "engine/singletonManager/singletonManager.h"

namespace NTT_NS
{
    NTT_DEFINE_SINGLETON(Renderer);

    Renderer::Renderer()
        : m_window(nullptr), m_shaderProgram(0), m_VAO(0), m_VBO(0)
    {
    }

    Renderer::~Renderer()
    {
    }

    void Renderer::Initialize()
    {
        if (glewInit() != GLEW_OK)
        {
            throw std::runtime_error("Failed to initialize GLEW");
        }

        const char *vertextShaderCode = R"(
            #version 330 core
            layout (location = 0) in vec3 aPos;
            void main()
            {
                gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
            }
        )";

        const char *fragmentShaderCode = R"(
            #version 330 core
            out vec4 FragColor;
            void main()
            {
                FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
            }
        )";

        // clang-format off
        float vertices[] = {
            -0.5f, -0.5f, 0.0f,
            0.5f, -0.5f, 0.0f,
            0.0f, 0.5f, 0.0f,
        };
        // clang-format on

        glGenBuffers(1, &m_VBO);
        glBindBuffer(GL_ARRAY_BUFFER, m_VBO);
        glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

        glGenVertexArrays(1, &m_VAO);
        glBindVertexArray(m_VAO);

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void *)0);
        glEnableVertexAttribArray(0);

        m_shaderProgram = glCreateProgram();
        unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
        glShaderSource(vertexShader, 1, &vertextShaderCode, NULL);
        glCompileShader(vertexShader);

        unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
        glShaderSource(fragmentShader, 1, &fragmentShaderCode, NULL);
        glCompileShader(fragmentShader);

        glAttachShader(m_shaderProgram, vertexShader);
        glAttachShader(m_shaderProgram, fragmentShader);
        glLinkProgram(m_shaderProgram);
        glDeleteShader(vertexShader);
        glDeleteShader(fragmentShader);
        glUseProgram(0);
    }

    void Renderer::Shutdown()
    {
        glDeleteProgram(m_shaderProgram);
        glDeleteBuffers(1, &m_VBO);
        glDeleteVertexArrays(1, &m_VAO);
    }

    void Renderer::Render()
    {
        // Before render
        glClearColor(1.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // Render
        glUseProgram(m_shaderProgram);
        glBindVertexArray(m_VAO);
        glDrawArrays(GL_TRIANGLES, 0, 3);
        glBindVertexArray(0);
        glUseProgram(0);

        // After render
    }

    void Renderer::Resize(unsigned int width, unsigned int height)
    {
        glViewport(0, 0, width, height);
    }
} // namespace NTT_NS
