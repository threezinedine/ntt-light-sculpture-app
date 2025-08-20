#include <GL/glew.h>
#include <glfw/glfw3.h>
#include <cstdio>
#include <stdexcept>
#include "engine/renderer/renderer.h"
#include "engine/singletonManager/singletonManager.h"
#include "engine/model/model.h"
#include "engine/logging/logging.h"

#include "shader.h"

namespace NTT_NS
{
    NTT_DEFINE_SINGLETON(Renderer);

    Renderer::Renderer()
        : m_window(nullptr), m_triangleVertexProgram(), m_lineVertexProgram(), m_modelID(INVALID_ID)
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

        auto version = glGetString(GL_VERSION);
        NTT_LOG_INFO("OpenGL version: %s", version);

        Face face1({
            Node(0, 0, 0),
            Node(0, 1, 0),
            Node(1, 0, 0),
        });

        Face face2({
            Node(0, 0, 0),
            Node(0, 1, 0),
            Node(0, 0, 1),
        });

        Face face3({
            Node(0, 0, 0),
            Node(1, 0, 0),
            Node(0, 0, 1),
        });

        Face face4({
            Node(0, 1, 0),
            Node(1, 0, 0),
            Node(0, 0, 1),
        });

        vector<Face> faces = {face1, face2, face3, face4};
        m_modelID = MODEL_NEW_BODY(faces);

        MODEL_TO_GPU(m_modelID);

        m_triangleVertexProgram.Append(MakeShader(GL_VERTEX_SHADER, triangleVertexShader));
        m_triangleVertexProgram.Append(MakeShader(GL_FRAGMENT_SHADER, triangleFragmentShader));
        m_triangleVertexProgram.Compile();

        m_lineVertexProgram.Append(MakeShader(GL_VERTEX_SHADER, lineVertexShader));
        m_lineVertexProgram.Append(MakeShader(GL_FRAGMENT_SHADER, lineFragmentShader));
        m_lineVertexProgram.Compile();

        glLineWidth(4.0f);
    }

    void Renderer::Shutdown()
    {
        MODEL_RELEASE(m_modelID);
    }

    void Renderer::StartDrawTriangle()
    {
        m_triangleVertexProgram.Use();
        m_triangleVertexProgram.SetUniform("u_view", Camera::GetInstance()->GetViewMatrix());
    }

    void Renderer::StartDrawLine()
    {
        m_lineVertexProgram.Use();
        m_lineVertexProgram.SetUniform("u_view", Camera::GetInstance()->GetViewMatrix());
    }

    void Renderer::Render()
    {
        // Before render
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // Render
        MODEL_DRAW(m_modelID);
        // After render
    }

    void Renderer::Resize(unsigned int width, unsigned int height)
    {
        m_width = width;
        m_height = height;
        glViewport(0, 0, width, height);
        Camera::GetInstance()->RecalculateViewMatrix();
    }
} // namespace NTT_NS
