#include "engine/model/face.h"
#include <stdexcept>
#include "engine/logging/logging.h"
#include "engine/singletonManager/singletonManager.h"

namespace NTT_NS
{
    vector<Face> FromFace(const Face &face)
    {
        vector<Face> finalFaces;
        vector<Node> nodes = face.nodes;
        Vec3 normal = face.normal;

        if (nodes.size() < 3)
        {
            throw std::runtime_error("Face must have at least 3 nodes.");
        }

        u32 startIndex = 0;

        while (nodes.size() != 3)
        {
            Position &firstNode = nodes[startIndex].position;
            Position &secondNode = nodes[startIndex + 1].position;
            Position &thirdNode = nodes[startIndex + 2].position;

            Vec3 edge1 = secondNode - firstNode;
            Vec3 edge2 = thirdNode - secondNode;

            glm::vec3 crossProduct = glm::cross(edge1.data(), edge2.data());
            if (glm::dot(crossProduct, normal.data()) < 0)
            {
                startIndex++;
                continue;
            }

            finalFaces.push_back(Face({firstNode, secondNode, thirdNode}));
            nodes.erase(nodes.begin() + startIndex + 1);

            startIndex = (startIndex + 1) % nodes.size();
        }

        finalFaces.push_back(Face(nodes));

        return finalFaces;
    }
} // namespace NTT_NS
