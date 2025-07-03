cmake_minimum_required(VERSION 3.16)
project(CppUnitTestGenerator VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Project description
set(PROJECT_DESCRIPTION "C++ Unit Test Generator using AI Models")

# Build options
option(BUILD_TESTS "Build tests" ON)
option(ENABLE_COVERAGE "Enable code coverage" ON)

# Set build type if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler flags
if(ENABLE_COVERAGE AND CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O0 --coverage")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
endif()

# Include directories
include_directories(src)

# Find source files
file(GLOB_RECURSE SOURCE_FILES "src/*.cpp")
file(GLOB_RECURSE HEADER_FILES "src/*.h")

# Create library from source files
add_library(${PROJECT_NAME}_lib ${SOURCE_FILES})

# Create main executable (if needed)
add_executable(${PROJECT_NAME} src/main.cpp)
target_link_libraries(${PROJECT_NAME} ${PROJECT_NAME}_lib)

# Testing configuration
if(BUILD_TESTS)
    enable_testing()
    
    # Find GTest
    find_package(GTest QUIET)
    if(GTest_FOUND)
        message(STATUS "Google Test found - tests will be built")
        
        # Add test directory
        add_subdirectory(tests)
    else()
        message(WARNING "Google Test not found - tests will not be built")
        message(STATUS "Install Google Test to enable testing")
    endif()
endif()

# Installation (optional)
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
)

install(FILES ${HEADER_FILES}
    DESTINATION include/${PROJECT_NAME}
)

# Print build information
message(STATUS "")
message(STATUS "=== Build Configuration ===")
message(STATUS "Project: ${PROJECT_NAME} v${PROJECT_VERSION}")
message(STATUS "Description: ${PROJECT_DESCRIPTION}")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Coverage enabled: ${ENABLE_COVERAGE}")
message(STATUS "Build tests: ${BUILD_TESTS}")
message(STATUS "==========================")
message(STATUS "") 