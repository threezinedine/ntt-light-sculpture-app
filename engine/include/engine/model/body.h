#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    struct Face;

    struct Body
    {
        vector<Face> faces;

        Body(const vector<Face> &faces)
            : faces(faces)
        {
        }
    };
} // namespace NTT_NS
