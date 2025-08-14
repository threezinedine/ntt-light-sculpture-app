#pragma once

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "engine/engine.h"

using namespace NTT_NS;

::testing::AssertionResult AssertVec3(const Vec3 &actual, const Vec3 &expected);