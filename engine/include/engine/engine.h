#pragma once
#include "common/common.h"
#include "logging/logging.h"
#include "utils/utils.h"
#include "renderer/renderer.h"
#include "singletonManager/singletonManager.h"
#include "model/model.h"

namespace NTT_NS
{
    class NTT_PYTHON_BINDING Engine
    {
    public:
        Engine();
        ~Engine();

        void Initialize() NTT_PYTHON_BINDING;
        void Update() NTT_PYTHON_BINDING;
        void Finalize() NTT_PYTHON_BINDING;

        NTT_DECLARE_PUBLIC_CLASS_PRIVATE_IMPL(Engine);
    };
} // namespace NTT_NS