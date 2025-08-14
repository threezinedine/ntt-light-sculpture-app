#include "engine/renderer/camera.h"
#include "engine/singletonManager/singletonManager.h"

namespace NTT_NS
{
    NTT_DEFINE_SINGLETON(Camera);

    Camera::Camera()
        : m_origin(Position(0.0f, 0.0f, 0.0f))
    {
    }

    Camera::~Camera()
    {
    }
} // namespace NTT_NS
