#pragma once
#include "macros.h"
#include <cstdint>
#include <string>
#include <cstring>
#include <cassert>
#include <memory>
#include <vector>
#include <map>
#include <set>
#include <chrono>
#include <functional>
#include <glm/glm.hpp>

typedef uint64_t u64;
static_assert(sizeof(u64) == 8, "u64 is not 8 bytes");
typedef uint32_t u32;
static_assert(sizeof(u32) == 4, "u32 is not 4 bytes");
typedef uint16_t u16;
static_assert(sizeof(u16) == 2, "u16 is not 2 bytes");
typedef uint8_t u8;
static_assert(sizeof(u8) == 1, "u8 is not 1 byte");

typedef int64_t i64;
static_assert(sizeof(i64) == 8, "i64 is not 8 bytes");
typedef int32_t i32;
static_assert(sizeof(i32) == 4, "i32 is not 4 bytes");
typedef int16_t i16;
static_assert(sizeof(i16) == 2, "i16 is not 2 bytes");
typedef int8_t i8;
static_assert(sizeof(i8) == 1, "i8 is not 1 byte");

typedef float f32;
static_assert(sizeof(f32) == 4, "f32 is not 4 bytes");
typedef double f64;
static_assert(sizeof(f64) == 8, "f64 is not 8 bytes");

typedef bool b8;
static_assert(sizeof(b8) == 1, "b8 is not 1 byte");

#define NTT_TRUE true
#define NTT_FALSE false

typedef std::string string;

template <typename T>
using vector = std::vector<T>;

template <typename K, typename V>
using map = std::map<K, V>;

template <typename T>
using set = std::set<T>;

template <typename T>
using Scope = ::std::unique_ptr<T>;

template <typename T, typename... Args>
inline Scope<T> CreateScope(Args &&...args)
{
    return std::make_unique<T>(std::forward<Args>(args)...);
}

template <typename T>
using Reference = ::std::shared_ptr<T>;

template <typename T, typename... Args>
inline Reference<T> CreateRef(Args &&...args)
{
    return std::make_shared<T>(std::forward<Args>(args)...);
}

template <typename T, typename... Args>
using Function = std::function<T(Args...)>;

#include "annotate.h"

typedef glm::vec2 Vec2;
typedef glm::vec3 Vec3;
typedef glm::vec4 Vec4;
typedef glm::mat2 Mat2;
typedef glm::mat3 Mat3;
typedef glm::mat4 Mat4;

#include "define.h"

const u32 INVALID_ID = u32(-1);

#include "assertion.h"