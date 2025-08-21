#include "engine/renderer/texture.h"
#include "GL/glew.h"
#include "textureShader.h"
#include "engine/logging/logging.h"

namespace NTT_NS
{
    Texture::Texture(f32 centerX, f32 centerY, f32 width, f32 height, u32 format)
        : m_centerX(centerX), m_centerY(centerY), m_width(width),
          m_height(height), m_format(format), m_program()
    {
        glGenTextures(1, &m_textureId);
        glBindTexture(GL_TEXTURE_2D, m_textureId);
        glTexStorage2D(GL_TEXTURE_2D, 1, m_format, width, height);

        // create texture rectangle
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

        glBindTexture(GL_TEXTURE_2D, 0); // Unbind the texture

        // clang-format off
        float rectangleVertices[] = {
            // Positions      // Texture Coords
            m_centerX - m_width / 2, m_centerY - m_height / 2, 0.0f, 0.0f,
            m_centerX + m_width / 2, m_centerY - m_height / 2, 1.0f, 0.0f,
            m_centerX + m_width / 2, m_centerY + m_height / 2, 1.0f, 1.0f,
            m_centerX - m_width / 2, m_centerY + m_height / 2, 0.0f, 1.0f,
        };

        u32 indexes[] = {
            1, 3, 0,
            1, 3, 2,
        };
        // clang-format on

        glGenBuffers(1, &m_vbo);
        glBindBuffer(GL_ARRAY_BUFFER, m_vbo);
        glBufferData(GL_ARRAY_BUFFER, sizeof(rectangleVertices), rectangleVertices, GL_STATIC_DRAW);

        glGenBuffers(1, &m_ebo);
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, m_ebo);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indexes), indexes, GL_STATIC_DRAW);

        glGenVertexArrays(1, &m_vao);
        glBindVertexArray(m_vao);

        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void *)0);
        glEnableVertexAttribArray(0);
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void *)(2 * sizeof(float)));
        glEnableVertexAttribArray(1);

        glBindVertexArray(0);

        // Program
        m_program.Append(MakeShader(GL_VERTEX_SHADER, textureVertexShader));
        m_program.Append(MakeShader(GL_FRAGMENT_SHADER, textureFragmentShader));
        m_program.Compile();
    }

    Texture::~Texture()
    {
        glDeleteTextures(1, &m_textureId);
        glDeleteBuffers(1, &m_vbo);
        glDeleteBuffers(1, &m_ebo);
        glDeleteVertexArrays(1, &m_vao);
    }

    void Texture::ToCompute(u32 index)
    {
        glBindTexture(GL_TEXTURE_2D, m_textureId);
        glBindImageTexture(index, m_textureId, 0, GL_FALSE, 0, GL_WRITE_ONLY, m_format);
    }

    void Texture::Draw()
    {
        m_program.Use();
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_2D, m_textureId);
        glBindVertexArray(m_vao);
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, m_ebo);

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
        glBindVertexArray(0);
    }
} // namespace NTT_NS
