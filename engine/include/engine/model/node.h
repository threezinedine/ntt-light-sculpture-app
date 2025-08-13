#pragma once
#include "engine/common/common.h"

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
    };
} // namespace NTT_NS
