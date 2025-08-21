#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    const char *textureVertexShader = R"(
#version 330 core

layout (location = 0) in vec2 aPos;
layout (location = 1) in vec2 vTexCoord;

out vec2 TexCoord;

void main()
{
    gl_Position = vec4(aPos, 0.0, 1.0);
    TexCoord = vTexCoord;
}
)";

    const char *textureFragmentShader = R"(
#version 330 core
out vec4 FragColor;

in vec2 TexCoord;

uniform sampler2D u_texture;

void main()
{
    FragColor = texture(u_texture, TexCoord);
}
)";

} // namespace NTT_NS
