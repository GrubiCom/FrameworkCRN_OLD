# Install script for directory: /home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/python

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
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/pmt_cpp" TYPE FILE FILES
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/python/__init__.py"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/python/PDU_json.py"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/python/data_extract_master.py"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/python/annp.py"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/python/cogmac.py"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/python/RandomForest.py"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/pmt_cpp" TYPE FILE FILES
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/__init__.pyc"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/PDU_json.pyc"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/data_extract_master.pyc"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/annp.pyc"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/cogmac.pyc"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/RandomForest.pyc"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/__init__.pyo"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/PDU_json.pyo"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/data_extract_master.pyo"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/annp.pyo"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/cogmac.pyo"
    "/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python/RandomForest.pyo"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

