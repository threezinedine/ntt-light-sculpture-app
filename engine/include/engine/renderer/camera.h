#pragma once
#include "engine/common/common.h"
#include "position.h"

namespace NTT_NS
{
    class NTT_PYTHON_BINDING NTT_SINGLETON Camera
    {
        NTT_DECLARE_SINGLETON(Camera);

    public:
        inline const Position &GetOrigin() const NTT_PYTHON_BINDING { return m_origin; }

    private:
        Position m_origin;
    };
} // namespace NTT_NS
