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
            NTT_ASSERT(nodes.size() >= 3);
            Node &node1 = this->nodes[0];
            Node &node2 = this->nodes[1];
            Node &node3 = this->nodes[2];
            Vec3 uv1 = node1 - node2;
            Vec3 uv2 = node2 - node3;
            glm::vec3 temporaryNormal = glm::normalize(glm::cross(uv1.data(), uv2.data()));
            normal.set(temporaryNormal.x, temporaryNormal.y, temporaryNormal.z);
        }

        Face(const Face &other)
            : normal(other.normal), nodes(other.nodes)
        {
        }
    };
} // namespace NTT_NS