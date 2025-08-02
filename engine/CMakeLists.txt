cmake_minimum_required(VERSION 3.20)

project(Engine)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

file(
    GLOB
    SOURCES
    "${CMAKE_CURRENT_SOURCE_DIR}/src/**/*.cpp"
)

file(
    GLOB 
    HEADERS
    "${CMAKE_CURRENT_SOURCE_DIR}/include/**/*.h"
)

# =================== externals ===================
set(CMAKE_FOLDER "externals")
find_package(ntt-opengl REQUIRED)
find_package(ntt-gtest REQUIRED)
unset(CMAKE_FOLDER)
# =====================================================

# =================== c++ libraries ===================
set(CMAKE_FOLDER "lib")
set(LIBRARY_NAME ${PROJECT_NAME}_LIB)
set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT ${LIBRARY_NAME})

add_library(${LIBRARY_NAME} STATIC ${SOURCES} ${HEADERS})
target_include_directories(${LIBRARY_NAME} PUBLIC include)
target_link_libraries(${LIBRARY_NAME} PUBLIC ntt-opengl)
set_target_properties(${LIBRARY_NAME} PROPERTIES CMAKE_POSITION_INDEPENDENT_CODE ON)
unset(CMAKE_FOLDER)
# =====================================================

# =================== python libraries ===================
set(CMAKE_FOLDER "binding")
find_package(pybind11 REQUIRED)
pybind11_add_module(${PROJECT_NAME} "binding.cpp")
target_link_libraries(${PROJECT_NAME} PRIVATE ${LIBRARY_NAME})
unset(CMAKE_FOLDER)
# ========================================================

# =================== test libraries ===================
set(CMAKE_FOLDER "test")
file(
    GLOB
    ENGINE_TEST_SOURCES
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/**/*.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/tests/*.cpp"
)

set(ENGINE_TEST_NAME "engine-test")
add_executable(${ENGINE_TEST_NAME} ${ENGINE_TEST_SOURCES})
target_link_libraries(${ENGINE_TEST_NAME} PRIVATE ntt-gtest)
unset(CMAKE_FOLDER)
# ========================================================

install(
    TARGETS ${LIBRARY_NAME}
    DESTINATION ${CMAKE_INSTALL_PREFIX}
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
    ARCHIVE DESTINATION lib
)


# =================== python libraries ===================
file(GLOB PYTHON_LIBRARIES "${CMAKE_CURRENT_BINARY_DIR}/Release/*.pyd")
install(
    FILES ${PYTHON_LIBRARIES}
    DESTINATION "${CMAKE_INSTALL_PREFIX}/python"
    RENAME "${PROJECT_NAME}.pyd"
)
# ========================================================