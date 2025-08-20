#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    const char *triangleVertexShader = R"(
#version 330 core

layout (location = 0) in vec3 aPos;
uniform mat4 u_view;

void main()
{
    gl_Position = u_view * vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
    )";

    const char *triangleFragmentShader = R"(
#version 330 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(0.5f, 0.5f, 0.5f, 0.5f);
}
)";

    const char *lineVertexShader = R"(
#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 u_view;

void main()
{
    gl_Position = u_view * vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
)";

    const char *lineFragmentShader = R"(
#version 330 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(0.0f, 0.0f, 1.0f, 1.0f);
}
)";
} // namespace NTT_NS
