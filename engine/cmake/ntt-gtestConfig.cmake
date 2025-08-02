set(BUILD_SHARED_LIBS OFF)
add_subdirectory(${CMAKE_SOURCE_DIR}/vendors/gtest)

set(NTT_GTEST_LIB_NAME "ntt-gtest")

add_library(${NTT_GTEST_LIB_NAME} INTERFACE)
target_link_libraries(
    ${NTT_GTEST_LIB_NAME} 
    INTERFACE 
    gtest
    gtest_main
    gmock
    gmock_main
)