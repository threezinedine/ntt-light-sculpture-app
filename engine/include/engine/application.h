#pragma once
#include "common/common.h"

namespace NTT_NS
{
    class Application
    {
    public:
        Application();
        ~Application();

        void Initialize() NTT_PYTHON_BINDING;
        void Resize(u32 width, u32 height) NTT_PYTHON_BINDING;
        void Update() NTT_PYTHON_BINDING;
        void Finalize() NTT_PYTHON_BINDING;

        NTT_DECLARE_PUBLIC_CLASS_PRIVATE_IMPL(Application);
    };
} // namespace NTT_NS