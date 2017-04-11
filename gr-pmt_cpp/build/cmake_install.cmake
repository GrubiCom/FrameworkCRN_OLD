# Install script for directory: /home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/usr/local")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "Release")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/pmt_cpp" TYPE FILE FILES "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/cmake/Modules/pmt_cppConfig.cmake")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  INCLUDE("/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/include/pmt_cpp/cmake_install.cmake")
  INCLUDE("/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/lib/cmake_install.cmake")
  INCLUDE("/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/swig/cmake_install.cmake")
  INCLUDE("/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/cmake_install.cmake")
  INCLUDE("/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/grc/cmake_install.cmake")
  INCLUDE("/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/apps/cmake_install.cmake")
  INCLUDE("/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/docs/cmake_install.cmake")

ENDIF(NOT CMAKE_INSTALL_LOCAL_ONLY)

IF(CMAKE_INSTALL_COMPONENT)
  SET(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
ELSE(CMAKE_INSTALL_COMPONENT)
  SET(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
ENDIF(CMAKE_INSTALL_COMPONENT)

FILE(WRITE "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/${CMAKE_INSTALL_MANIFEST}" "")
FOREACH(file ${CMAKE_INSTALL_MANIFEST_FILES})
  FILE(APPEND "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/${CMAKE_INSTALL_MANIFEST}" "${file}\n")
ENDFOREACH(file)
