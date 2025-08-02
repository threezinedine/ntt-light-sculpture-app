#pragma once
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include "engine/common/common.h"

namespace NTT_NS
{
    /**
     * @brief The renderer class is responsible for rendering the scene.
     */
    class Renderer
    {
    public:
        Renderer();
        ~Renderer();

        /**
         * @brief Initialize the renderer
         * Should be run once at the beginning of the application, this method will
         *      start and configure all the needed components, resources (like shaders, textures, etc.)
         *      and set up the window.
         *
         * @note This method must be called before any other method inside this class.
         */
        void Initialize();

        /**
         * @brief Shutdown the renderer
         * Should be run once at the end of the application, this method will
         * clean up the window and the OpenGL context.
         */
        void Shutdown();

        void BeforeRender();
        void AfterRender();

        /**
         * @brief Render the scene for every frame
         * This method will be called every frame, it will render the scene and update the window.
         *
         * @note This method must be called every frame.
         */
        void Render();

    private:
        /**
         * The window that will be used to render the scene.
         */
        GLFWwindow *m_window;
    };
}