#include "engine/renderer/position.h"

namespace NTT_NS
{
    Position::Position()
        : m_data(0.0f, 0.0f, 0.0f)
    {
    }

    Position::Position(float x, float y, float z)
        : m_data(x, y, z)
    {
    }

    Position::Position(const Position &other)
        : m_data(other.m_data)
    {
    }

    Position::~Position()
    {
    }
} // namespace NTT_NS
