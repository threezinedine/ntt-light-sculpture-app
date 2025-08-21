#include <GL/glew.h>
#include <glfw/glfw3.h>
#include <cstdio>
#include <stdexcept>
#include "engine/renderer/renderer.h"
#include "engine/singletonManager/singletonManager.h"
#include "engine/model/model.h"
#include "engine/logging/logging.h"
#include "engine/renderer/texture.h"
#include "shader.h"

namespace NTT_NS
{
    NTT_DEFINE_SINGLETON(Renderer);

    Renderer::Renderer()
        : m_window(nullptr), m_triangleVertexProgram(), m_lineVertexProgram(), m_rayTracerProgram(), m_modelID(INVALID_ID)
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

        // vector<Face> faces = {face1, face2, face3, face4};
        vector<Face> faces = {face1, face2, face3};
        m_modelID = MODEL_NEW_BODY(faces);

        MODEL_TO_GPU(m_modelID);

        m_triangleVertexProgram.Append(MakeShader(GL_VERTEX_SHADER, triangleVertexShader));
        m_triangleVertexProgram.Append(MakeShader(GL_FRAGMENT_SHADER, triangleFragmentShader));
        m_triangleVertexProgram.Compile();

        m_lineVertexProgram.Append(MakeShader(GL_VERTEX_SHADER, lineVertexShader));
        m_lineVertexProgram.Append(MakeShader(GL_FRAGMENT_SHADER, lineFragmentShader));
        m_lineVertexProgram.Compile();

        m_rayTracerProgram.Append(MakeShader(GL_COMPUTE_SHADER, rayTracingComputeShader));
        m_rayTracerProgram.Compile();

#if 1
        m_rayTracerProgram.Use();
        ModelContainer::GetInstance()->ToCompute(1, {m_modelID});
#endif

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
        if (m_texture)
        {
            m_rayTracerProgram.Use();
            m_rayTracerProgram.SetUniform("u_cameraOrigin", Camera::GetInstance()->GetOrigin().data());
            m_rayTracerProgram.SetUniform("u_upVector", Camera::GetInstance()->GetUpVector().data());
            m_rayTracerProgram.SetUniform("u_rightVector", Camera::GetInstance()->GetRightVector().data());
            m_texture->ToCompute(0);
#if 0
            ModelContainer::GetInstance()->ToCompute(1);
#endif
            vector<FaceData> readData(3);
            glGetBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, readData.size() * sizeof(FaceData), readData.data());
            glDispatchCompute((GetWidth() + 7) / 8, (GetHeight() + 7) / 8, 1);
            glMemoryBarrier(GL_SHADER_IMAGE_ACCESS_BARRIER_BIT);

            m_texture->Draw();
        }

        MODEL_DRAW(m_modelID);
        // After render
    }

    void Renderer::Resize(unsigned int width, unsigned int height)
    {
        m_width = width;
        m_height = height;
        if (m_texture)
        {
            m_texture.reset(); // Reset the texture if it already exists
        }
        m_texture = CreateScope<Texture>(0.0f, 0.0f, 2.0f, 2.0f, GetWidth(), GetHeight(), GL_RGBA8);
        glViewport(0, 0, width, height);
        Camera::GetInstance()->RecalculateViewMatrix();
    }
} // namespace NTT_NS
