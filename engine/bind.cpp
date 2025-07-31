#include "pybind11/pybind11.h"
#include "engine/engine.h"

using namespace pybind11;

PYBIND11_MODULE(Engine, m)
{
    m.doc() = "Engine module";
    m.def("add", &ntt::add, "Add two numbers");
}