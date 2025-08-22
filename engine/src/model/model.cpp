#include "engine/model/model.h"
#include "engine/container/container.h"
#include "engine/singletonManager/singletonManager.h"
#include <cstdio>
#include <GL/glew.h>
#include "engine/logging/logging.h"

namespace NTT_NS
{
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
        m_shaderBuffer = 0;                                                    // Initialize the shader storage buffer ID to 0
    }

    ModelContainer::~ModelContainer()
    {
        if (m_shaderBuffer)
        {
            glDeleteBuffers(1, &m_shaderBuffer); // Clean up the shader storage buffer
        }
    }

    u32 ModelContainer::CreateBody(const vector<Face> &faces)
    {
        u32 id = m_bodies->Create((void *)&faces);

        m_bodyIds.push_back(id); // Store the ID of the created body

        return id;
    }

    u32 ModelContainer::ToCompute(u32 index)
    {
        return ToCompute(index, m_bodyIds);
    }

    u32 ModelContainer::ToCompute(u32 index, const vector<u32> &bodyIds)
    {
        vector<FaceData> faceData;

        for (const auto &bodyId : bodyIds)
        {
            Body *body = GET_BODY(bodyId);
            body->ToCompute(faceData);
        }

        for (const auto &face : faceData)
        {
            NTT_ASSERT(abs(glm::dot(face.normal, face.nodes[0] - face.nodes[1])) < 1e-3);
            NTT_ASSERT(abs(glm::dot(face.normal, face.nodes[1] - face.nodes[2])) < 1e-3);
            NTT_ASSERT(abs(glm::dot(face.normal, face.nodes[2] - face.nodes[0])) < 1e-3);
        }

        if (m_shaderBuffer == 0)
        {
            glGenBuffers(1, &m_shaderBuffer);
            glBindBuffer(GL_SHADER_STORAGE_BUFFER, m_shaderBuffer);
            glBufferData(GL_SHADER_STORAGE_BUFFER, faceData.size() * sizeof(FaceData), faceData.data(), GL_STATIC_DRAW);
        }
        else
        {
            glBindBuffer(GL_SHADER_STORAGE_BUFFER, m_shaderBuffer);
            glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, faceData.size() * sizeof(FaceData), faceData.data());
        }

        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, index, m_shaderBuffer);

        return faceData.size();
    }
} // namespace NTT_NS
