# Find spot, a platform for LTL and ω-automata manipulation
# See https://spot.lrde.epita.fr

# This file is included in ltlsynth from OMPL project <https://github.com/ompl/ompl>.

INCLUDE(FindPackageHandleStandardArgs)

FIND_PACKAGE(PkgConfig)
if(PKGCONFIG_FOUND)
    pkg_check_modules(SPOT libspot)
    if(SPOT_LIBRARIES AND NOT SPOT_INCLUDE_DIRS)
        set(SPOT_INCLUDE_DIRS "/usr/local/include")
    endif()
endif()
find_package_handle_standard_args(SPOT DEFAULT_MSG SPOT_LIBRARIES SPOT_INCLUDE_DIRS)