#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    struct Node;

    struct Face
    {
        Vec3 normal;
        vector<Node> nodes;

        Face(const vector<Node> &nodes)
            : nodes(nodes)
        {
            normal = Vec3(0.0f, 0.0f, 0.0f); // Default normal, will be calculated based on nodes
        }

        Face(const Face &other)
            : normal(other.normal), nodes(other.nodes)
        {
        }
    };
} // namespace NTT_NS