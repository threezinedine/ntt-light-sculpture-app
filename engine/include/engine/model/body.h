#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    struct Face;

    class Body
    {
    public:
        Body(const vector<Face> &faces);
        ~Body();

        /**
         * This method is only be used for debugging purposes. If Body is null
         *      do nothing.
         */
        void PrintModel();

        /**
         * Call once at the config stage for starting to rendering the body.
         */
        void ToGPU();

        /**
         * Used for delete all needed resources like vertex buffer and vertex array on both
         *      GPU and cpu side. Should be call if the Body is pushed into GPU.
         */
        void Release();

        /**
         * Be called in every frame to render the body
         */
        void Draw();

        /**
         * Transfer all the triangles and their normals to the compute shader for ray tracing purpose
         *
         * @param index The binding index for the compute shader (see more in `example`)
         *
         * @example
         * ```c++
         * Body body;
         *
         * body.ToCompute(1); // binding to position 1 (layout std430, binding = 1)
         * ```
         */
        void ToCompute(u32 index = 0);

    private:
        vector<Face> m_faces;
        u32 m_vao;
        u32 m_vbo;
        u32 m_vertexCount;

        u32 m_lineVao;
        u32 m_lineVbo;
        u32 m_lineVertexCount;
    };
} // namespace NTT_NS
