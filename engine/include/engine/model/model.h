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

        u32 CreateBody(const vector<Face> &faces);

        /**
         * Passing all bodies to the compute shader
         *
         * @param index The binding index for the compute shader (see more in `example`)
         *
         * @return number of triangles passed to the compute shader
         */
        u32 ToCompute(u32 index);

        /**
         * Passing all body faces into the compute shader for ray tracing
         *
         * @param index The binding index for the compute shader (see more in `example`)
         *
         * @return number of triangles passed to the compute shader
         *
         * @example
         * ```c++
         * u32 bodyId = MODEL_NEW_BODY(faces);
         *
         * ModelContainer::GetInstance()->ToCompute(1, {bodyId}); // data will be passed into (layout std430, binding = 1)
         * ```
         */
        u32 ToCompute(u32 index, const vector<u32> &bodyIds);

    private:
        Scope<Container<Body>> m_bodies;
        vector<u32> m_bodyIds; // Store the IDs of bodies for easy access
        u32 m_shaderBuffer;
    };
} // namespace NTT_NS

#define GET_BODY(bodyId) (NTT_NS::ModelContainer::GetInstance()->GetBodies()->Get(bodyId))
#define MODEL_NEW_BODY(faces) NTT_NS::ModelContainer::GetInstance()->CreateBody(faces)
#define MODEL_TO_GPU(bodyId) (GET_BODY(bodyId))->ToGPU()
#define MODEL_RELEASE(bodyId) (GET_BODY(bodyId))->Release()
#define MODEL_DRAW(bodyId) (GET_BODY(bodyId))->Draw()