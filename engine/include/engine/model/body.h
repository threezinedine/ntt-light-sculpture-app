#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    struct Face;
/**
 * The data which will be sent to the GPU for computing shader
 *      The main usage of it is used for ray tracing
 */
#pragma pack(push, 1)
    struct FaceData
    {
        glm::vec4 normal;
        glm::vec4 nodes[3];
    };
#pragma pack(pop)

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
         * @param faceData The face data to be transferred, the data will be added into this array.
         *
         * @example
         * ```c++
         * Body body;
         * vector<FaceData> faceData = {}; // contains all other triangles
         *
         * body.ToCompute(faceData);
         * ```
         */
        void ToCompute(vector<FaceData> &faceData);

    private:
        vector<Face> m_faces;
        u32 m_vao;
        u32 m_vbo;
        u32 m_vertexCount;

        u32 m_lineVao;
        u32 m_lineVbo;
        u32 m_lineVertexCount;

        /**
         * @brief The buffer used for passing data to the compute shader
         */
        u32 m_shaderBuffer;
    };
} // namespace NTT_NS
