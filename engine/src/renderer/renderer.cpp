#include <GL/glew.h>
#include <glfw/glfw3.h>
#include <cstdio>
#include <stdexcept>
#include "engine/renderer/renderer.h"
#include "engine/singletonManager/singletonManager.h"
#include "engine/model/model.h"

namespace NTT_NS
{
    NTT_DEFINE_SINGLETON(Renderer);

    Renderer::Renderer()
        : m_window(nullptr), m_shaderProgram(), m_modelID(INVALID_ID)
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

        Node node1(1, 0, 0);
        Node node2(0.5f, -0.5f, 0);
        Node node3(0, 0.5f, 0);
        Node node4(0.5f, -0.5f, 0);
        Node node5(0, 0.5f, 0);
        Node node6(-1, 0, 0);
        Face face1({node1, node2, node3});
        Face face2({node4, node5, node6});

        vector<Face> faces = {face1, face2};
        m_modelID = MODEL_NEW_BODY(faces);

        MODEL_TO_GPU(m_modelID);

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
        MODEL_RELEASE(m_modelID);
    }

    void Renderer::Render()
    {
        // Before render
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // Render
        m_shaderProgram.Use();
        MODEL_DRAW(m_modelID);
        // After render
    }

    void Renderer::Resize(unsigned int width, unsigned int height)
    {
        glViewport(0, 0, width, height);
    }
} // namespace NTT_NS
