cmake_minimum_required(VERSION 3.9)
set(PROJECT_NAME "ck_pathcobbler_bindings")
set(CMAKE_CXX_STANDARD 17)
project(${PROJECT_NAME})

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

file(GLOB_RECURSE ckutils_executable_sources CONFIGURE_DEPENDS
     "${PROJECT_SOURCE_DIR}/ck_utilities/src/*.cpp"
)

set(INT_LIB_NAME "ck_utilities")
add_library(${INT_LIB_NAME} STATIC ${ckutils_executable_sources})
set_property(TARGET ${INT_LIB_NAME} PROPERTY POSITION_INDEPENDENT_CODE ON)
target_include_directories(${INT_LIB_NAME} PUBLIC "ck_utilities/include")
target_link_libraries(${INT_LIB_NAME} Threads::Threads)

file(GLOB_RECURSE executable_sources CONFIGURE_DEPENDS
     "${PROJECT_SOURCE_DIR}/src/*.cpp"
)

add_library(${PROJECT_NAME} SHARED ${executable_sources})
target_include_directories(${PROJECT_NAME} PUBLIC "include" "ck_utilities/include")
target_link_libraries(${PROJECT_NAME} Threads::Threads ${INT_LIB_NAME})
#add_dependencies(${PROJECT_NAME} ${${PROJECT_NAME}_EXPORTED_TARGETS})
