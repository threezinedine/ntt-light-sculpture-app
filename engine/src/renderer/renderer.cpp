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
        : m_window(nullptr), m_shaderProgram(), m_VAO(0), m_VBO(0)
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

        m_shaderProgram.AddVertexShader(
            R"(
            #version 330 core
            layout (location = 0) in vec3 aPos;
            void main()
            {
                gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
            }
        )");

        m_shaderProgram.AddFragmentShader(
            R"(
            #version 330 core
            out vec4 FragColor;
            void main()
            {
                FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
            }
        )");

        m_shaderProgram.Compile();
    }

    void Renderer::Shutdown()
    {
        glDeleteBuffers(1, &m_VBO);
        glDeleteVertexArrays(1, &m_VAO);
    }

    void Renderer::Render()
    {
        // Before render
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // Render
        m_shaderProgram.Use();
        glBindVertexArray(m_VAO);
        glDrawArrays(GL_TRIANGLES, 0, 3);
        glBindVertexArray(0);

        // After render
    }

    void Renderer::Resize(unsigned int width, unsigned int height)
    {
        glViewport(0, 0, width, height);
    }
} // namespace NTT_NS
