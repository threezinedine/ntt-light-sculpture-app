#pragma once
#include "common/common.h"

namespace NTT_NS
{
    class Application
    {
    public:
        Application();
        ~Application();

        void Initialize();
        void Resize(u32 width, u32 height);
        void Update();
        void Finalize();

        NTT_DECLARE_PUBLIC_CLASS_PRIVATE_IMPL(Application);
    };
} // namespace NTT_NS