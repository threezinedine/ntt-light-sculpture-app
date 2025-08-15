#pragma once
#include "engine/common/common.h"
#include "engine/renderer/position.h"

namespace NTT_NS
{
    struct Node
    {
        Position position;

        Node(float x = 0, float y = 0, float z = 0)
            : position(x, y, z)
        {
        }
        Node(const Position &pos)
            : position(pos)
        {
        }

        Node(const Node &other)
            : position(other.position)
        {
        }

        Vec3 operator-(const Node &other) const
        {
            return Vec3(position.x() - other.position.x(),
                        position.y() - other.position.y(),
                        position.z() - other.position.z());
        }
    };
} // namespace NTT_NS
