#pragma once
#include "engine/common/common.h"

#include "node.h"
#include "face.h"
#include "body.h"

namespace NTT_NS
{
    /**
     * This method is only be used for debugging purposes.
     */
    void PrintModel(const Body &body);

    /**
     * Call once at the config stage for starting to rendering the body.
     *
     * @param body The body to be rendered.
     * @param id The ID of the vertex buffer object that will be created for the body.
     * @param vertexCount the number of nodes in the body.
     */
    void ToGPU(const Body &body, u32 &id, u32 &vertexCount);
} // namespace NTT_NS
