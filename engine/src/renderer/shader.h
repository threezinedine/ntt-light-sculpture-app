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

#pragma pack(push, 1)
struct Triangle
{
    vec4 normal;
    vec4 points[3];
};
#pragma pack(pop)

layout (local_size_x = 8, local_size_y = 8) in;

layout (rgba8, binding = 0) uniform image2D renderedOutput;
layout (std430, binding = 1) buffer TriangleBuffer
{
    Triangle triangles[];
};

uniform vec3 u_cameraOrigin;
uniform vec3 u_upVector;
uniform vec3 u_rightVector;
uniform float u_factor;
uniform uint u_triangleCount;

vec3 intersectByT(vec3 rayVector, float t)
{
    return u_cameraOrigin + t * rayVector;
}

float findRayIntersectWithFace(vec3 rayVector, Triangle triangle)
{
    vec3 faceNormal = triangle.normal.xyz; // (0, 0, -1)
    vec3 facePoint = triangle.points[0].xyz; // (0, 0, 0)

    float denom = dot(rayVector, faceNormal); // 5

    if (abs(denom) < 1e-6)
    {
        return -1;
    }

    float t = dot((facePoint - u_cameraOrigin), faceNormal) / denom; // 1

    if (t < 0)
    {
        return -1;
    }

    return t;
}

bool isBetween(vec3 point1, vec3 point2, vec3 testPoint)
{
    vec3 dir1 = testPoint - point1;
    vec3 dir2 = testPoint - point2;

    float dotProduct = dot(dir1, dir2);

    return dotProduct <= 0;
}

int isInsideTriangle(float t, vec3 rayVector, Triangle triangle)
{
    vec3 P = intersectByT(rayVector, t);
    vec3 A = triangle.points[0].xyz; // (0, 0, 0)
    vec3 B = triangle.points[1].xyz; // (0, 1, 0)
    vec3 C = triangle.points[2].xyz; // (1, 0, 0)
    vec3 normal = normalize(triangle.normal.xyz); // (0, 0, -1)

    vec3 AB = B - A; // (0, 1, 0)
    vec3 BC = C - B; // (1, -1, 0)
    vec3 CA = A - C; // (-1, 0, 0)

    vec3 n1 = cross(AB, normal); // (-1, 0, 0)
    vec3 n2 = cross(BC, normal); // (1, 1, 0)
    vec3 n3 = cross(CA, normal); // (0, -1, 0)

    // (0.1, 0.1, 0)
    vec3 AP = P - A; // (0.1, 0.1, 0)
    vec3 BP = P - B; // (0.1, -0.9, 0)
    vec3 CP = P - C; // (-0.9, 0.1, 0)

    float v1 = dot(AP, n1); // -0.1
    float v2 = dot(BP, n2); // -0.8
    float v3 = dot(CP, n3); // -0.1

    float epsilon = 1e-2;

    if (abs(v1) < epsilon && isBetween(A, B, P))
    {
        return 1; 
    }

    if (abs(v2) < epsilon && isBetween(B, C, P))
    {
        return 1;
    }

    if (abs(v3) < epsilon && isBetween(C, A, P))
    {
        return 1;
    }

    if (v1 < 0 && v2 < 0 && v3 < 0)
    {
        return -1;
    }

    if (v1 > 0 && v2 > 0 && v3 > 0)
    {
        return -1;
    }

    return 0;
}

bool compareFloat(float a, float b)
{
    return abs(a - b) < 1e-6;
}

bool compareVec4(vec4 a, vec4 b)
{
    return compareFloat(a.x, b.x) && compareFloat(a.y, b.y) && compareFloat(a.z, b.z) && compareFloat(a.w, b.w);
}

void main()
{
    ivec2 pixelCoords = ivec2(gl_GlobalInvocationID.xy);
    ivec2 textureSize = imageSize(renderedOutput);

    if (pixelCoords.x < 0 || pixelCoords.x >= textureSize.x || pixelCoords.y < 0 || pixelCoords.y >= textureSize.y)
    {
        return;
    }

    vec3 rayTarget = - (float(pixelCoords.x) - float(textureSize.x) / 2.0) / u_factor * normalize(u_rightVector) +
                     (float(pixelCoords.y) - float(textureSize.y) / 2.0) / u_factor * normalize(u_upVector);

    vec3 rayVector = normalize(rayTarget - u_cameraOrigin); // (0, 0, -5)

    float t = -1;
    vec4 color = vec4(1.0);

    for (uint triangleIndex = 0u; triangleIndex < u_triangleCount; ++triangleIndex)
    {
        float tempT = findRayIntersectWithFace(rayVector, triangles[triangleIndex]);

        if (tempT <= 0)
        {
            continue;
        }

        if (tempT > t && t >= 0)
        {
            continue; 
        }

        int inside = isInsideTriangle(tempT, rayVector, triangles[triangleIndex]);

        if (inside == 1)
        {
            color = vec4(1, 0.0, 0.0, 0.5);
            t = tempT;
        }
        else if (inside == -1)
        {
            color = vec4(0.0, 0.0, 1, 0.5);
            t = tempT;
        }
        else 
        {
            if (t < 0)
            {
                color = vec4(0.3, 0.3, 0.3, 0.5);
            }
        }
    }

    imageStore(renderedOutput, pixelCoords, color);
}
)";

} // namespace NTT_NS
