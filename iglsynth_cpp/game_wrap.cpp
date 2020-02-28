//
// Created by abhibp1993 on 2/21/20.
//

#include <boost/python.hpp>

#include "util/entity.h"
#include "game/action.h"


#define IGLSYNTH_FRAMEWORK_VERSION  "1.0.0"


namespace IGLSynth {

// Current version of ltlsynth framework
    std::string version() { return IGLSYNTH_FRAMEWORK_VERSION; }


    BOOST_PYTHON_MODULE (iglsynth) {
        namespace bp = boost::python;
        bp::def("version", version);

        // Specify that this module is actually a package
        bp::object module = bp::scope();
        module.attr("__path__") = "iglsynth";

        // Wrap Entity Class
        namespace bp = boost::python;

        // map the core namespace to a sub-module
        // make "from ltlsynth.core import ____" work
        bp::object coreModule(bp::handle<>(bp::borrowed(PyImport_AddModule("iglsynth.game"))));

        // make "from ltlsynth import core" work
        bp::scope().attr("game") = coreModule;

        // set the current scope to the new sub-module
        bp::scope util_scope = coreModule;

        // Import Classes, Functions
        bp::class_<Entity>("_Entity")
                .add_property("id", &Entity::id)
                .def("to_string", &Entity::tostring)
                .def("serialize", &Entity::serialize)
                .def("__str__", &Entity::tostring);

        bp::class_<Action, bp::bases<Entity>>("Action", bp::init<const std::string, std::string>())
                .def_readwrite("desc", &Action::desc)
                .def("serialize", &Entity::serialize)
                .def("deserialize", &Entity::deserialize)
                ;

    }
}