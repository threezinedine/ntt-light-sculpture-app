#pragma once
#include "engine/common/common.h"
#include "engine/container/container.h"

#include "node.h"
#include "face.h"
#include "body.h"

namespace NTT_NS
{
    class ModelContainer
    {
        NTT_DECLARE_SINGLETON(ModelContainer);
        NTT_NON_COPYABLE(ModelContainer);

    public:
        inline const Scope<Container<Body>> &GetBodies() const { return m_bodies; }

    private:
        Scope<Container<Body>> m_bodies;
    };
} // namespace NTT_NS

#define MODEL_NEW_BODY(faces) NTT_NS::ModelContainer::GetInstance()->GetBodies()->Create(&(faces))
#define MODEL_TO_GPU(bodyId) (NTT_NS::ModelContainer::GetInstance()->GetBodies()->Get(bodyId))->ToGPU()
#define MODEL_RELEASE(bodyId) (NTT_NS::ModelContainer::GetInstance()->GetBodies()->Get(bodyId))->Release()
#define MODEL_DRAW(bodyId) (NTT_NS::ModelContainer::GetInstance()->GetBodies()->Get(bodyId))->Draw()