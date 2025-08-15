#pragma once
#include "engine/common/common.h"
#include "position.h"

namespace NTT_NS
{
    class NTT_PYTHON_BINDING NTT_SINGLETON Camera
    {
        NTT_DECLARE_SINGLETON(Camera);

    public:
        inline const Position &GetOrigin() const NTT_PYTHON_BINDING;
        void Move(const Vec3 &direction, f32 dt) NTT_PYTHON_BINDING;

        inline const Mat4 &GetViewMatrix() const { return m_viewMatrix; }

    private:
        void RecalculateViewMatrix();

    private:
        Position m_origin;
        Mat4 m_viewMatrix;
    };

    const Position &Camera::GetOrigin() const
    {
        return m_origin;
    }
} // namespace NTT_NS
