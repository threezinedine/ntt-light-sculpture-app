set(GLM_DIR "${CMAKE_CURRENT_SOURCE_DIR}/vendors/glm")
add_subdirectory(${GLM_DIR})

add_library(ntt-glm INTERFACE)
target_link_libraries(ntt-glm INTERFACE glm)
target_include_directories(ntt-glm INTERFACE ${GLM_DIR})