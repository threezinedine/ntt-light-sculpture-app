#include "engine/renderer/camera.h"
#include "engine/singletonManager/singletonManager.h"
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include "engine/renderer/renderer.h"
#include "engine/renderer/program.h"

namespace NTT_NS
{
    NTT_DEFINE_SINGLETON(Camera);

    Camera::Camera()
        : m_origin(1.0f, 1.0f, 2.0f)
    {
        RecalculateViewMatrix();
    }

    Camera::~Camera()
    {
    }

    void Camera::RecalculateViewMatrix()
    {
        Position target(0.0f, 0.0f, 0.0f); // Always look at the origin
        Vec3 up = Vec3(0.0f, 1.0f, 0.0f);
        Mat4 viewMatrix = glm::lookAt(m_origin.data(), target.data(), up.data());

        // Project matrix
        f32 fov = glm::radians(45.0f);
        float aspectRatio = f32(Renderer::GetInstance()->GetWidth()) / f32(Renderer::GetInstance()->GetHeight());
        float nearPlane = 0.1f;
        float farPlane = 100.0f;
        Mat4 projectionMatrix = glm::perspective(fov, aspectRatio, nearPlane, farPlane);

        m_viewMatrix = projectionMatrix * viewMatrix; // Combine projection and view matrices
    }

    void Camera::Move(const Vec3 &direction, f32 dt)
    {
        m_origin += direction * dt;
        RecalculateViewMatrix();
    }

    template <>
    void Program::SetUniform(const string &name, const Mat4 &value)
    {
        glUseProgram(m_programID);
        GLuint location = glGetUniformLocation(m_programID, name.c_str());
        glUniformMatrix4fv(location, 1, GL_FALSE, glm::value_ptr(value));
    }
} // namespace NTT_NS
