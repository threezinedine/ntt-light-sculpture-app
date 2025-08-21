#include "engine/renderer/camera.h"
#include "engine/singletonManager/singletonManager.h"
#include <glm/gtc/matrix_transform.hpp>
#include "engine/renderer/renderer.h"
#include "engine/renderer/program.h"

namespace NTT_NS
{
    NTT_DEFINE_SINGLETON(Camera);

    Camera::Camera()
        : m_origin(1.0f, 1.0f, 2.0f),
          m_up(0.0f, 1.0f, 0.0f),
          m_right(1.0f, 0.0f, 0.0f),
          m_target(0.0f, 0.0f, 0.0f)
    {
        RecalculatePolarCoordinates();
        RecalculateViewMatrix();
    }

    Camera::~Camera()
    {
    }

    void Camera::RecalculatePolarCoordinates()
    {
        Vec3 diff = m_origin - m_target;
        m_distance = m_origin.DistanceFrom(m_target);
        m_phi = glm::atan(diff.y() / diff.z());
        m_theta = glm::atan(diff.x() / diff.z());
    }

    void Camera::RecalculateUpVector()
    {
        if (m_origin.z() == 0)
        {
            return;
        }

        float x = m_origin.x();
        float y = m_origin.y();
        float z = m_origin.z();

        glm::vec3 direction = glm::normalize(glm::vec3(-z * x / (x * x + y * y), -z * y / (x * x + y * y), 1.0f));

        m_up.set(direction.x, direction.y, direction.z);
    }

    void Camera::RecalculateRightVector()
    {
        glm::vec3 right = glm::cross(m_up.data(), -m_origin.data());
        m_right.set(right.x, right.y, right.z);
    }

    void Camera::RecalculateViewMatrix()
    {
        RecalculateUpVector();
        RecalculateRightVector();
        Mat4 viewMatrix = glm::lookAt(m_origin.data(), m_target.data(), m_up.data());
        // Mat4 viewMatrix = glm::lookAt(m_origin.data(), m_target.data(), glm::vec3(0, 0, 1));

        // Project matrix
        f32 fov = glm::radians(45.0f);
        float aspectRatio = f32(Renderer::GetInstance()->GetWidth()) / f32(Renderer::GetInstance()->GetHeight());
        float nearPlane = 0.1f;
        float farPlane = 100.0f;
        Mat4 projectionMatrix = glm::perspective(fov, aspectRatio, nearPlane, farPlane);

        m_viewMatrix = projectionMatrix * viewMatrix; // Combine projection and view matrices
    }

    void Camera::RecalculateTheOrigin()
    {
        m_origin = Position(m_distance * glm::sin(m_phi) * glm::cos(m_theta),
                            m_distance * glm::sin(m_phi) * glm::sin(m_theta),
                            m_distance * glm::cos(m_phi));
    }

    void Camera::SetOrigin(const Position &origin)
    {
        m_origin = origin;
        RecalculatePolarCoordinates();
        RecalculateViewMatrix();
    }

    void Camera::Move(const Vec3 &direction, f32 dt)
    {
        f32 factor = dt;

        m_phi -= direction.y() * factor;
        m_theta -= direction.x() * factor;

        float twoPi = glm::pi<float>() * 2;

        if (m_phi < 0)
        {
            m_phi += twoPi;
        }
        else if (m_phi > glm::pi<float>())
        {
            m_phi -= twoPi;
        }

        if (m_theta < 0)
        {
            m_theta += twoPi;
        }
        else if (m_theta > twoPi)
        {
            m_theta -= twoPi;
        }

        RecalculateTheOrigin();
        RecalculateViewMatrix();
    }
} // namespace NTT_NS
