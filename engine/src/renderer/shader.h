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

vec3 findRayIntersectWithFace(vec3 rayVector, Triangle triangle)
{
    vec3 faceNormal = triangle.normal.xyz; // (0, 0, -1)
    vec3 facePoint = triangle.points[0].xyz; // (0, 0, 0)

    float denom = dot(rayVector, faceNormal); // 5

    if (abs(denom) < 1e-6)
    {
        return vec3(1e30); // Ray is parallel to the face
    }

    float t = dot((facePoint - u_cameraOrigin), faceNormal) / denom; // 1

    if (t < 0)
    {
        return vec3(1e30); // Intersection is behind the camera
    }

    return u_cameraOrigin + t * rayVector; // (0, 0, 0)
}

int isInsideTriangle(vec3 P, Triangle triangle)
{
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

    float epsilon = 1e-3;

    if (abs(v1) < epsilon || abs(v2) < epsilon || abs(v3) < epsilon)
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

    float factor = 600;
    vec3 rayTarget = - (float(pixelCoords.x) - float(textureSize.x) / 2.0) / factor * normalize(u_rightVector) +
                     (float(pixelCoords.y) - float(textureSize.y) / 2.0) / factor * normalize(u_upVector);

    vec3 rayVector = normalize(rayTarget - u_cameraOrigin); // (0, 0, -5)

    vec3 intersect = findRayIntersectWithFace(rayVector, triangles[0]);

    if (length(intersect) > 1e29)
    {
        imageStore(renderedOutput, pixelCoords, vec4(1, 0, 0, 1));
        return;
    }

    int inside = isInsideTriangle(intersect, triangles[0]);

    if (inside == 1)
    {
        imageStore(renderedOutput, pixelCoords, vec4(1, 0.5, 0.5, 0.4));
    }
    else if (inside == -1)
    {
        imageStore(renderedOutput, pixelCoords, vec4(0.5, 0.5, 1, 1));
    }
    else 
    {
        imageStore(renderedOutput, pixelCoords, vec4(0.3, 0.3, 0.3, 1));
    }
}
)";

} // namespace NTT_NS
