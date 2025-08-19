#pragma once
#include "engine/common/common.h"
#include "position.h"

namespace NTT_NS
{
    class NTT_PYTHON_BINDING NTT_SINGLETON Camera
    {
        NTT_DECLARE_SINGLETON(Camera);

    public:
        /**
         * @brief Get the camera origin.
         *
         * @return The camera origin.
         */
        inline const Position &GetOrigin() const NTT_PYTHON_BINDING;

        /**
         * @brief Be called at the beginning of the project.
         *
         * @param origin The new camera origin. If the origin is (0, 0, 0), the camera will be placed at the
         *      default position (1, 1, 2), this origin will not be limited by the fixed size as the `Move` method.
         */
        void SetOrigin(const Position &origin) NTT_PYTHON_BINDING;

        /**
         * @brief Translate the camera origin. This is used for tracking the mouse from the Python
         *
         * @param direction The delta vector which the camera will be moved by (based on the current view of the camera).
         * @param dt The time delta since the last frame.
         */
        void Move(const Vec3 &direction, f32 dt) NTT_PYTHON_BINDING;

        inline const Mat4 &GetViewMatrix() const { return m_viewMatrix; }

        void RecalculateViewMatrix();

    private:
        void RecalculateTheOrigin(f32 originalDistance);

    private:
        Position m_origin;
        Position m_target; // Always look at the this point.
        Mat4 m_viewMatrix;
        Vec3 m_upVector; // Indicate the rotation of the camera.
    };

    const Position &Camera::GetOrigin() const
    {
        return m_origin;
    }
} // namespace NTT_NS
