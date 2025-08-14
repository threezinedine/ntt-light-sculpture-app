#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    struct Face;

    struct Body
    {
        vector<Face> faces;
        u32 vao;
        u32 vbo;
        u32 vertexCount;

        u32 lineVao;
        u32 lineVbo;
        u32 lineVertexCount;

        Body(const vector<Face> &faces)
            : faces(faces), vao(0), vbo(0), vertexCount(0), lineVao(0), lineVbo(0), lineVertexCount(0)
        {
        }
    };
} // namespace NTT_NS
