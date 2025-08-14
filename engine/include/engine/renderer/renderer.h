#pragma once
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include "engine/common/common.h"
#include "engine/renderer/program.h"
#include "camera.h"

namespace NTT_NS
{
    /**
     * @brief The renderer class is responsible for rendering the scene.
     */
    class NTT_PYTHON_BINDING NTT_SINGLETON Renderer
    {
        NTT_DECLARE_SINGLETON(Renderer);

    public:
        /**
         * @brief Initialize the renderer
         * Should be run once at the beginning of the application, this method will
         *      start and configure all the needed components, resources (like shaders, textures, etc.)
         *      and set up the window.
         *
         * @note This method must be called before any other method inside this class.
         */
        void Initialize() NTT_PYTHON_BINDING;

        /**
         * @brief Shutdown the renderer
         * Should be run once at the end of the application, this method will
         * clean up the window and the OpenGL context.
         */
        void Shutdown() NTT_PYTHON_BINDING;

        /**
         * @brief Render the scene for every frame
         * This method will be called every frame, it will render the scene and update the window.
         *
         * @note This method must be called every frame.
         */
        void Render() NTT_PYTHON_BINDING;

        /**
         * @brief Resize the window
         * This method will be called when the size of the window is changed,
         *      it will update the viewport and the projection matrix.
         *
         * @param width The new width of the window.
         * @param height The new height of the window.
         */
        void Resize(u32 width, u32 height) NTT_PYTHON_BINDING;

        inline void StartDrawTriangle() { m_triangleVertexProgram.Use(); };
        inline void StartDrawLine() { m_lineVertexProgram.Use(); };

        inline b8 ShouldDrawEdges() const;
        inline void SetShouldDrawEdges(b8 value) NTT_PYTHON_BINDING;

        inline b8 ShouldDrawFaces() const;
        inline void SetShouldDrawFaces(b8 value) NTT_PYTHON_BINDING;

    private:
        /**
         * The window that will be used to render the scene.
         */
        GLFWwindow *m_window;

        Program m_triangleVertexProgram; // Shader program used for rendering
        Program m_lineVertexProgram;     // Shader program used for rendering
        u32 m_modelID;
        b8 m_shouldDrawEdges;
        b8 m_shouldDrawFaces;
    };

    b8 Renderer::ShouldDrawEdges() const { return m_shouldDrawEdges; }
    void Renderer::SetShouldDrawEdges(b8 value) { m_shouldDrawEdges = value; }

    b8 Renderer::ShouldDrawFaces() const { return m_shouldDrawFaces; }
    void Renderer::SetShouldDrawFaces(b8 value) { m_shouldDrawFaces = value; }
}