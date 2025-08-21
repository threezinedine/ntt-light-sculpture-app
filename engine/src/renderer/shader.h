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

    const char *rayTracingComputeShader = R"(
#version 430 core    

struct Triangle
{
    vec3 points[3];
};

layout (local_size_x = 8, local_size_y = 8) in;

layout (rgba8, binding = 0) uniform image2D renderedOutput;
layout (std430, binding = 1) buffer TriangleBuffer
{
    Triangle triangles[];
};

uniform vec3 u_cameraOrigin;
uniform float u_viewAngle;

void main()
{
    ivec2 pixelCoords = ivec2(gl_GlobalInvocationID.xy);
    ivec2 textureSize = imageSize(renderedOutput);

    if (pixelCoords.x < 0 || pixelCoords.x >= textureSize.x || pixelCoords.y < 0 || pixelCoords.y >= textureSize.y)
    {
        return;
    }

    // random a color
    vec4 color = vec4(
        float(pixelCoords.x) / float(textureSize.x),
        float(pixelCoords.y) / float(textureSize.y),
        0.0f,
        1.0f
    );

    imageStore(renderedOutput, pixelCoords, color);
}
)";

} // namespace NTT_NS
