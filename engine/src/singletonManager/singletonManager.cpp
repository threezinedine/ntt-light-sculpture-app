#include "engine/singletonManager/singletonManager.h"

namespace NTT_NS
{
    vector<void *> SingletonManager::s_instances;
    vector<SingletonDestroyCallback> SingletonManager::s_destroyCallbacks;

    void SingletonManager::Initialize()
    {
    }

    void SingletonManager::Finalize()
    {
        u32 instanceCount = s_instances.size();
        for (u32 i = 0; i < instanceCount; i++)
        {
            s_destroyCallbacks[i](s_instances[i]);
        }
        s_instances.clear();
        s_destroyCallbacks.clear();
    }

    void SingletonManager::RegisterSingleton(void *instance, SingletonDestroyCallback callback)
    {
        s_instances.push_back(instance);
        s_destroyCallbacks.push_back(callback);
    }
} // namespace NTT_NS