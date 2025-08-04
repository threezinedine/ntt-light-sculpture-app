#include "engine/application.h"
#include "engine/singletonManager/singletonManager.h"
#include "engine/logging/logging.h"
#include "engine/renderer/renderer.h"
#include "engine/renderer/renderer.h"

namespace NTT_NS
{
    class Application::ApplicationImpl
    {
    public:
    };

    Application::Application()
    {
        m_impl = CreateScope<ApplicationImpl>();
    }

    Application::~Application()
    {
    }

    void Application::Initialize()
    {
        SingletonManager::Initialize();

        Renderer::GetInstance()->Initialize();

        NTT_LOG_INFO("Application initialized");
    }

    void Application::Resize(u32 width, u32 height)
    {
        Renderer::GetInstance()->Resize(width, height);
    }

    void Application::Update()
    {
        Renderer::GetInstance()->Render();
    }

    void Application::Finalize()
    {
        NTT_LOG_INFO("Application finalized");

        Renderer::GetInstance()->Shutdown();

        SingletonManager::Finalize();
    }
} // namespace NTT_NS