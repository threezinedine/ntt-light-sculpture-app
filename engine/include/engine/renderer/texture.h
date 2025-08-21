#pragma once
#include "engine/common/common.h"
#include "GL/glew.h"
#include "program.h"

namespace NTT_NS
{
    /**
     * Used for displaying the 2D textures which is output from ray tracing process.
     */
    class Texture
    {
    public:
        Texture(f32 centerX, f32 centerY, f32 width, f32 height,
                u32 textureWidth, u32 textureHeight, u32 format = GL_RGBA8);
        ~Texture();

        inline f32 GetWidth() const { return m_width; }
        inline f32 GetHeight() const { return m_height; }

        /**
         * Binding to the compute shader
         *
         * @param index The binding index for the compute shader (used in (layout binding = index))
         */
        void ToCompute(u32 index = 0);

        /**
         * Render the texture on the screen
         */
        void Draw();

    private:
        f32 m_centerX;
        f32 m_centerY;
        f32 m_width;
        f32 m_height;

        u32 m_format;

        u32 m_textureId;
        u32 m_vbo;
        u32 m_ebo;
        u32 m_vao;

        Program m_program; ///< The shader program used for rendering the texture
    };
} // namespace NTT_NS
