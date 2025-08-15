#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "engine/engine.h"
#include "ntt_assertion.h"

using namespace NTT_NS;

TEST(FaceTest, Auto_Create_Normal_Vector_From_Input_Nodes)
{
    Node node1(0, 0, 0);
    Node node2(1, 0, 0);
    Node node3(0, 1, 0);
    Face face({node1, node2, node3});

    EXPECT_TRUE(AssertVec3(face.normal, Vec3(0, 0, 1)));
}