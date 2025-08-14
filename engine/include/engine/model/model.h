#pragma once
#include "engine/common/common.h"
#include "engine/container/container.h"

#include "node.h"
#include "face.h"
#include "body.h"

namespace NTT_NS
{
    /**
     * This method is only be used for debugging purposes.
     */
    void PrintModel(Body *body);

    /**
     * Call once at the config stage for starting to rendering the body.
     *
     * @param body The body to be rendered.
     * @param id The ID of the vertex buffer object that will be created for the body.
     * @param vertexCount the number of nodes in the body.
     */
    void ToGPU(Body *body);

    void Release(Body *body);
    void Draw(Body *body);

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
#define MODEL_TO_GPU(bodyId) NTT_NS::ToGPU(NTT_NS::ModelContainer::GetInstance()->GetBodies()->Get(bodyId))
#define MODEL_RELEASE(bodyId) NTT_NS::Release(NTT_NS::ModelContainer::GetInstance()->GetBodies()->Get(bodyId))
#define MODEL_DRAW(bodyId) NTT_NS::Draw(NTT_NS::ModelContainer::GetInstance()->GetBodies()->Get((bodyId)))