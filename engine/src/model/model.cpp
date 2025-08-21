#include "engine/model/model.h"
#include "engine/container/container.h"
#include "engine/singletonManager/singletonManager.h"
#include <cstdio>
#include <GL/glew.h>

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
    }

    ModelContainer::~ModelContainer()
    {
    }

    u32 ModelContainer::CreateBody(const vector<Face> &faces)
    {
        u32 id = m_bodies->Create((void *)&faces);

        m_bodyIds.push_back(id); // Store the ID of the created body

        return id;
    }

    void ModelContainer::ToCompute(u32 index)
    {
        ToCompute(index, m_bodyIds);
    }

    void ModelContainer::ToCompute(u32 index, const vector<u32> &bodyIds)
    {
        vector<FaceData> faceData;

        for (const auto &bodyId : bodyIds)
        {
            Body *body = GET_BODY(bodyId);
            body->ToCompute(faceData);
        }

        glGenBuffers(1, &m_shaderBuffer);
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, m_shaderBuffer);
        glBufferData(GL_SHADER_STORAGE_BUFFER, faceData.size() * sizeof(FaceData), faceData.data(), GL_STATIC_DRAW);
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, index, m_shaderBuffer);
    }
} // namespace NTT_NS
