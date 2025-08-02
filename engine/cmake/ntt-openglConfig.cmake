set(glew-cmake_BUILD_STATIC ON)
set(glew-cmake_BUILD_SHARED_LIBS OFF)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/vendors/glew)

set(BUILD_SHARED_LIBS OFF)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/vendors/glfw)

find_package(OpenGL REQUIRED)

set(NTT_OPENGGL_LIBNAME ntt-opengl)

add_library(${NTT_OPENGGL_LIBNAME} INTERFACE)
target_link_libraries(
    ${NTT_OPENGGL_LIBNAME} 
    INTERFACE 
    glfw
    libglew_static 
    OpenGL::GL
)
set_target_properties(${NTT_OPENGGL_LIBNAME} PROPERTIES FOLDER "Externals")