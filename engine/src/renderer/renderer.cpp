#include <GL/glew.h>
#include <stdexcept>
#include <glfw/glfw3.h>
#include "engine/renderer/renderer.h"

namespace NTT_NS
{
    Renderer::Renderer()
        : m_window(nullptr)
    {
    }

    Renderer::~Renderer()
    {
    }

    void Renderer::Initialize()
    {
    }

    void Renderer::Shutdown()
    {
    }

    void Renderer::BeforeRender()
    {
        glClearColor(1.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
    }

    void Renderer::AfterRender()
    {
    }

    void Renderer::Render()
    {
    }
} // namespace NTT_NS
