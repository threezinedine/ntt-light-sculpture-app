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

        Body(const vector<Face> &faces)
            : faces(faces), vao(0), vbo(0), vertexCount(0)
        {
        }
    };
} // namespace NTT_NS
