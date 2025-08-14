#include "engine/model/model.h"
#include "engine/container/container.h"
#include "engine/singletonManager/singletonManager.h"
#include <cstdio>
#include <GL/glew.h>
#include "engine/renderer/renderer.h"

namespace NTT_NS
{
    void PrintModel(Body *body)
    {
        printf("Body:\n");
        u32 faceCount = body->faces.size();
        for (u32 faceIndex = 0; faceIndex < faceCount; ++faceIndex)
        {
            printf("\tFace: %d\n - Normal vector: (%f, %f, %f)\n", faceIndex,
                   body->faces[faceIndex].normal.x,
                   body->faces[faceIndex].normal.y,
                   body->faces[faceIndex].normal.z);

            u32 nodeCount = body->faces[faceIndex].nodes.size();
            for (u32 nodeIndex = 0; nodeIndex < nodeCount; ++nodeIndex)
            {
                printf("\t\tNode: (%f, %f, %f)\n", body->faces[faceIndex].nodes[nodeIndex].position.x(),
                       body->faces[faceIndex].nodes[nodeIndex].position.y(),
                       body->faces[faceIndex].nodes[nodeIndex].position.z());
            }

            printf("\tEnd Face\n");
        }

        printf("End Body\n");
    }

    void ToGPU(Body *body)
    {
        body->vertexCount = 0;

        u32 faceCount = body->faces.size();
        for (u32 faceIndex = 0; faceIndex < faceCount; ++faceIndex)
        {
            u32 nodeCount = body->faces[faceIndex].nodes.size();
            for (u32 nodeIndex = 0; nodeIndex < nodeCount; ++nodeIndex)
            {
                body->vertexCount++;
            }
        }

        body->lineVertexCount = body->vertexCount * 2; // Each node will be connected to the next one

        vector<float> vertexData;
        vertexData.resize(body->vertexCount * 3); // 3 components per node (x, y, z)
        u32 vertexIndex = 0;

        vector<float> lineData;
        lineData.resize(body->vertexCount * 2 * 3); // 3 components per node (x, y, z)
        u32 lineDataIndex = 0;

        for (u32 faceIndex = 0; faceIndex < faceCount; ++faceIndex)
        {
            u32 nodeCount = body->faces[faceIndex].nodes.size();
            for (u32 nodeIndex = 0; nodeIndex < nodeCount; ++nodeIndex)
            {
                Position pos = body->faces[faceIndex].nodes[nodeIndex].position;

                vertexData[vertexIndex++] = pos.x();
                vertexData[vertexIndex++] = pos.y();
                vertexData[vertexIndex++] = pos.z();

                lineData[lineDataIndex++] = pos.x();
                lineData[lineDataIndex++] = pos.y();
                lineData[lineDataIndex++] = pos.z();

                u32 nextNodeIndex = (nodeIndex + 1) % nodeCount; // Wrap around to the first node if at the end of the face
                Position nextPos = body->faces[faceIndex].nodes[nextNodeIndex].position;
                lineData[lineDataIndex++] = nextPos.x();
                lineData[lineDataIndex++] = nextPos.y();
                lineData[lineDataIndex++] = nextPos.z();
            }
        }

        // Upload vertexData to GPU and get the vertex buffer ID
        glGenBuffers(1, &body->vbo);
        glBindBuffer(GL_ARRAY_BUFFER, body->vbo);
        glBufferData(GL_ARRAY_BUFFER, vertexData.size() * sizeof(float), vertexData.data(), GL_STATIC_DRAW);

        glGenVertexArrays(1, &body->vao);
        glBindVertexArray(body->vao);

        glBindBuffer(GL_ARRAY_BUFFER, body->vbo);
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void *)0);
        glEnableVertexAttribArray(0);

        glGenBuffers(1, &body->lineVbo);
        glBindBuffer(GL_ARRAY_BUFFER, body->lineVbo);
        glBufferData(GL_ARRAY_BUFFER, lineData.size() * sizeof(float), lineData.data(), GL_STATIC_DRAW);

        glGenVertexArrays(1, &body->lineVao);
        glBindVertexArray(body->lineVao);
        glBindBuffer(GL_ARRAY_BUFFER, body->lineVbo);
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void *)0);
        glEnableVertexAttribArray(0);
        glBindVertexArray(0);
    }

    void Release(Body *body)
    {
        if (body->vbo != 0)
        {
            glDeleteBuffers(1, &body->vbo);
            body->vbo = 0;
        }

        if (body->vao != 0)
        {
            glDeleteVertexArrays(1, &body->vao);
            body->vao = 0;
        }
    }

    void Draw(Body *body)
    {
        if (Renderer::GetInstance()->ShouldDrawFaces())
        {
            Renderer::GetInstance()->StartDrawTriangle();
            glBindVertexArray(body->vao);
            glDrawArrays(GL_TRIANGLES, 0, body->vertexCount);
        }

        if (Renderer::GetInstance()->ShouldDrawEdges())
        {
            Renderer::GetInstance()->StartDrawLine();
            glBindVertexArray(body->lineVao);
            glDrawArrays(GL_LINES, 0, body->lineVertexCount);
        }

        glBindVertexArray(0);
    }

    NTT_DEFINE_SINGLETON(ModelContainer);

    static Body *AllocateBody(void *data)
    {
        return new Body(*static_cast<vector<Face> *>(data));
    }

    static void DeallocateBody(Body *body)
    {
        delete body;
    }

    ModelContainer::ModelContainer()
    {
        m_bodies = CreateScope<Container<Body>>(AllocateBody, DeallocateBody); // Initialize with a capacity of 100 bodies
    }

    ModelContainer::~ModelContainer()
    {
    }
} // namespace NTT_NS
