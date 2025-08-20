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
} // namespace NTT_NS
