#pragma once

#define NTT_NS ntt

/**
 * This macro is stick with the `SingletonManager` module whereas
 *      the `SingletonManager` module is used for managing the singleton instances of the engine.
 * Each time a singleton is registered or created, the `SingletonManager` will has the responsibility
 *      for deleting it when the engine is shutting down.
 */
#define NTT_DECLARE_SINGLETON(className) \
private:                                 \
    static className *s_instance;        \
                                         \
public:                                  \
    static className *GetInstance();     \
                                         \
private:                                 \
    className();                         \
                                         \
public:                                  \
    ~className();

#define NTT_DEFINE_SINGLETON(className)                        \
    className *className::s_instance = nullptr;                \
    className *className::GetInstance()                        \
    {                                                          \
        if (s_instance == nullptr)                             \
        {                                                      \
            s_instance = new className();                      \
            SingletonManager::RegisterSingleton(               \
                s_instance,                                    \
                [](void *instance)                             \
                {                                              \
                    delete static_cast<className *>(instance); \
                });                                            \
        }                                                      \
        return s_instance;                                     \
    }

/**
 * Provide the way to hide all private members of the class from the .h
 *      file so that the modification of the private members will not affect other .h files.
 */
#define NTT_DECLARE_PUBLIC_CLASS_PRIVATE_IMPL(className) \
private:                                                 \
    class className##Impl;                               \
    Scope<className##Impl> m_impl;