#include "engine/engine.h"
#include "engine/singletonManager/singletonManager.h"
#include "engine/logging/logging.h"
#include "engine/renderer/renderer.h"
#include "engine/renderer/renderer.h"

namespace NTT_NS
{
    class Engine::EngineImpl
    {
    public:
    };

    Engine::Engine()
    {
        m_impl = CreateScope<EngineImpl>();
    }

    Engine::~Engine()
    {
    }

    void Engine::Initialize()
    {
        SingletonManager::Initialize();

        NTT_LOG_INFO("Engine initialized");
    }

    void Engine::Update()
    {
    }

    void Engine::Finalize()
    {
        NTT_LOG_INFO("Engine finalized");

        SingletonManager::Finalize();
    }
} // namespace NTT_NS