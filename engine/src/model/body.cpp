#include "engine/model/face.h"
#include "engine/model/node.h"
#include "engine/model/body.h"
#include <GL/glew.h>
#include "engine/renderer/renderer.h"
#include "engine/logging/logging.h"

namespace NTT_NS
{
    Body::Body(const vector<Face> &faces)
        : m_faces(faces), m_vao(0), m_vbo(0), m_vertexCount(0),
          m_lineVao(0), m_lineVbo(0), m_lineVertexCount(0)
    {
    }

    Body::~Body()
    {
    }

    void Body::PrintModel()
    {
        printf("Body:\n");
        u32 faceCount = m_faces.size();
        for (u32 faceIndex = 0; faceIndex < faceCount; ++faceIndex)
        {
            printf("\tFace: %d\n - Normal vector: (%f, %f, %f)\n", faceIndex,
                   m_faces[faceIndex].normal.x(),
                   m_faces[faceIndex].normal.y(),
                   m_faces[faceIndex].normal.z());

            u32 nodeCount = m_faces[faceIndex].nodes.size();
            for (u32 nodeIndex = 0; nodeIndex < nodeCount; ++nodeIndex)
            {
                printf("\t\tNode: (%f, %f, %f)\n", m_faces[faceIndex].nodes[nodeIndex].position.x(),
                       m_faces[faceIndex].nodes[nodeIndex].position.y(),
                       m_faces[faceIndex].nodes[nodeIndex].position.z());
            }

            printf("\tEnd Face\n");
        }

        printf("End Body\n");
    }

    void Body::ToGPU()
    {
        m_vertexCount = 0;

        u32 faceCount = m_faces.size();
        for (u32 faceIndex = 0; faceIndex < faceCount; ++faceIndex)
        {
            u32 nodeCount = m_faces[faceIndex].nodes.size();
            for (u32 nodeIndex = 0; nodeIndex < nodeCount; ++nodeIndex)
            {
                m_vertexCount++;
            }
        }

        m_lineVertexCount = m_vertexCount * 2; // Each node will be connected to the next one

        vector<float> vertexData;
        vertexData.resize(m_vertexCount * 3); // 3 components per node (x, y, z)
        u32 vertexIndex = 0;

        vector<float> lineData;
        lineData.resize(m_vertexCount * 2 * 3); // 3 components per node (x, y, z)
        u32 lineDataIndex = 0;

        for (u32 faceIndex = 0; faceIndex < faceCount; ++faceIndex)
        {
            u32 nodeCount = m_faces[faceIndex].nodes.size();
            for (u32 nodeIndex = 0; nodeIndex < nodeCount; ++nodeIndex)
            {
                Position pos = m_faces[faceIndex].nodes[nodeIndex].position;

                vertexData[vertexIndex++] = pos.x();
                vertexData[vertexIndex++] = pos.y();
                vertexData[vertexIndex++] = pos.z();

                lineData[lineDataIndex++] = pos.x();
                lineData[lineDataIndex++] = pos.y();
                lineData[lineDataIndex++] = pos.z();

                u32 nextNodeIndex = (nodeIndex + 1) % nodeCount; // Wrap around to the first node if at the end of the face
                Position nextPos = m_faces[faceIndex].nodes[nextNodeIndex].position;
                lineData[lineDataIndex++] = nextPos.x();
                lineData[lineDataIndex++] = nextPos.y();
                lineData[lineDataIndex++] = nextPos.z();
            }
        }

        // Upload vertexData to GPU and get the vertex buffer ID
        glGenBuffers(1, &m_vbo);
        glBindBuffer(GL_ARRAY_BUFFER, m_vbo);
        glBufferData(GL_ARRAY_BUFFER, vertexData.size() * sizeof(float), vertexData.data(), GL_STATIC_DRAW);

        glGenVertexArrays(1, &m_vao);
        glBindVertexArray(m_vao);

        glBindBuffer(GL_ARRAY_BUFFER, m_vao);
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void *)0);
        glEnableVertexAttribArray(0);

        glGenBuffers(1, &m_lineVbo);
        glBindBuffer(GL_ARRAY_BUFFER, m_lineVbo);
        glBufferData(GL_ARRAY_BUFFER, lineData.size() * sizeof(float), lineData.data(), GL_STATIC_DRAW);

        glGenVertexArrays(1, &m_lineVao);
        glBindVertexArray(m_lineVao);
        glBindBuffer(GL_ARRAY_BUFFER, m_lineVbo);
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void *)0);
        glEnableVertexAttribArray(0);
        glBindVertexArray(0);
    }

    void Body::Release()
    {
        if (m_vbo != 0)
        {
            glDeleteBuffers(1, &m_vbo);
            m_vbo = 0;
        }

        if (m_vao != 0)
        {
            glDeleteVertexArrays(1, &m_vao);
            m_vao = 0;
        }

        if (m_lineVbo != 0)
        {
            glDeleteBuffers(1, &m_lineVbo);
            m_lineVbo = 0;
        }

        if (m_lineVao != 0)
        {
            glDeleteVertexArrays(1, &m_lineVao);
            m_lineVao = 0;
        }

        if (m_shaderBuffer != 0)
        {
            glDeleteBuffers(1, &m_shaderBuffer);
            m_shaderBuffer = 0;
        }
    }

    void Body::Draw()
    {
        if (Renderer::GetInstance()->ShouldDrawFaces())
        {
            Renderer::GetInstance()->StartDrawTriangle();
            glBindVertexArray(m_vao);
            glDrawArrays(GL_TRIANGLES, 0, m_vertexCount);
        }

        if (Renderer::GetInstance()->ShouldDrawEdges())
        {
            Renderer::GetInstance()->StartDrawLine();
            glBindVertexArray(m_lineVao);
            glDrawArrays(GL_LINES, 0, m_lineVertexCount);
        }

        glBindVertexArray(0);
    }

    void Body::ToCompute(vector<FaceData> &faceData)
    {
        u32 offset = faceData.size();
        u32 faceCount = m_faces.size();
        faceData.resize(offset + faceCount);

        for (u32 faceIndex = offset; faceIndex < offset + faceCount; ++faceIndex)
        {
            FaceData data;
            data.normal = glm::vec4(m_faces[faceIndex].normal.data(), 0.0);
            data.nodes[0] = glm::vec4(m_faces[faceIndex].nodes[0].position.data(), 0.0);
            data.nodes[1] = glm::vec4(m_faces[faceIndex].nodes[1].position.data(), 0.0);
            data.nodes[2] = glm::vec4(m_faces[faceIndex].nodes[2].position.data(), 0.0);
            faceData[faceIndex] = data;
        }
    }

} // namespace NTT_NS
