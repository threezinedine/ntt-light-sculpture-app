cmake_minimum_required(VERSION 3.20)

project(Engine)

if (MSVC)
    set_property(GLOBAL PROPERTY USE_FOLDERS ON)
endif()

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

file(
    GLOB
    SOURCES
    src/**/*.cpp
)

# =================== c++ libraries ===================
set(CMAKE_FOLDER "lib")
set(LIBRARY_NAME ${PROJECT_NAME}_LIB)

add_library(${LIBRARY_NAME} STATIC ${SOURCES})
target_include_directories(${LIBRARY_NAME} PUBLIC include)
unset(CMAKE_FOLDER)
# =====================================================

# =================== python libraries ===================
set(CMAKE_FOLDER "binding")
find_package(pybind11 REQUIRED)
pybind11_add_module(${PROJECT_NAME} "bind.cpp")
target_link_libraries(${PROJECT_NAME} PRIVATE ${LIBRARY_NAME})
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