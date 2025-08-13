#include "engine/model/model.h"
#include <cstdio>
#include <GL/glew.h>

namespace NTT_NS
{
    void PrintModel(const Body &body)
    {
        printf("Body:\n");
        u32 faceCount = body.faces.size();
        for (u32 faceIndex = 0; faceIndex < faceCount; ++faceIndex)
        {
            printf("\tFace: %d\n - Normal vector: (%f, %f, %f)\n", faceIndex,
                   body.faces[faceIndex].normal.x,
                   body.faces[faceIndex].normal.y,
                   body.faces[faceIndex].normal.z);

            u32 nodeCount = body.faces[faceIndex].nodes.size();
            for (u32 nodeIndex = 0; nodeIndex < nodeCount; ++nodeIndex)
            {
                printf("\t\tNode: (%f, %f, %f)\n", body.faces[faceIndex].nodes[nodeIndex].position.x,
                       body.faces[faceIndex].nodes[nodeIndex].position.y,
                       body.faces[faceIndex].nodes[nodeIndex].position.z);
            }

            printf("\tEnd Face\n");
        }

        printf("End Body\n");
    }

    void ToGPU(const Body &body, u32 &id, u32 &vertexCount)
    {
        vertexCount = 0;

        u32 faceCount = body.faces.size();
        for (u32 faceIndex = 0; faceIndex < faceCount; ++faceIndex)
        {
            u32 nodeCount = body.faces[faceIndex].nodes.size();
            for (u32 nodeIndex = 0; nodeIndex < nodeCount; ++nodeIndex)
            {
                vertexCount++;
            }
        }

        vector<float> vertexData;
        vertexData.resize(vertexCount * 3); // 3 components per node (x, y, z)
        u32 vertexIndex = 0;

        for (u32 faceIndex = 0; faceIndex < faceCount; ++faceIndex)
        {
            u32 nodeCount = body.faces[faceIndex].nodes.size();
            for (u32 nodeIndex = 0; nodeIndex < nodeCount; ++nodeIndex)
            {
                vertexData[vertexIndex++] = body.faces[faceIndex].nodes[nodeIndex].position.x;
                vertexData[vertexIndex++] = body.faces[faceIndex].nodes[nodeIndex].position.y;
                vertexData[vertexIndex++] = body.faces[faceIndex].nodes[nodeIndex].position.z;
            }
        }

        // Upload vertexData to GPU and get the vertex buffer ID
        glGenBuffers(1, &id);
        glBindBuffer(GL_ARRAY_BUFFER, id);
        glBufferData(GL_ARRAY_BUFFER, vertexData.size() * sizeof(float), vertexData.data(), GL_STATIC_DRAW);
    }
} // namespace NTT_NS
