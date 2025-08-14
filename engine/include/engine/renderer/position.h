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
        inline void setX(float x) NTT_PYTHON_BINDING;

        inline const float y() const NTT_PYTHON_BINDING;
        inline void setY(float y) NTT_PYTHON_BINDING;

        inline const float z() const NTT_PYTHON_BINDING;
        inline void setZ(float z) NTT_PYTHON_BINDING;

        inline void set(float x, float y, float z) NTT_PYTHON_BINDING;

        inline glm::vec3 &data();

    private:
        Vec3 m_data;
    };

    const float Position::x() const
    {
        return m_data.x;
    }

    void Position::setX(float x)
    {
        m_data.x = x;
    }

    const float Position::y() const
    {
        return m_data.y;
    }

    void Position::setY(float y)
    {
        m_data.y = y;
    }

    const float Position::z() const
    {
        return m_data.z;
    }

    void Position::setZ(float z)
    {
        m_data.z = z;
    }

    void Position::set(float x, float y, float z)
    {
        setX(x);
        setY(y);
        setZ(z);
    }

    glm::vec3 &Position::data()
    {
        return m_data;
    }
} // namespace NTT_NS
