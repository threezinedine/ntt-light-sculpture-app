#pragma once
#include "engine/common/common.h"

namespace NTT_NS
{
    class NTT_PYTHON_BINDING Position
    {
    public:
        Position();
        Position(float x, float y, float z);
        Position(const Position &other);
        ~Position();

        inline const float x() const NTT_PYTHON_BINDING;
        inline const float y() const NTT_PYTHON_BINDING;
        inline const float z() const NTT_PYTHON_BINDING;

    private:
        Vec3 m_data;
    };

    const float Position::x() const { return m_data.x; }
    const float Position::y() const { return m_data.y; }
    const float Position::z() const { return m_data.z; }
} // namespace NTT_NS
