import pytest
from utils.types import TypeConverter


@pytest.fixture
def rawConverter() -> TypeConverter:
    return TypeConverter()


def test_convert_raw_type(rawConverter: TypeConverter):
    # ============== Integer types ==============
    assert rawConverter.convertType("int") == "int"
    assert rawConverter.convertType("int32_t") == "int"
    assert rawConverter.convertType("int64_t") == "int"
    assert rawConverter.convertType("int16_t") == "int"
    assert rawConverter.convertType("int8_t") == "int"
    assert rawConverter.convertType("uint32_t") == "int"
    assert rawConverter.convertType("uint64_t") == "int"
    assert rawConverter.convertType("uint16_t") == "int"
    assert rawConverter.convertType("uint8_t") == "int"
    assert rawConverter.convertType("unsigned int") == "int"
    assert rawConverter.convertType("unsigned long") == "int"
    assert rawConverter.convertType("unsigned short") == "int"
    assert rawConverter.convertType("unsigned char") == "int"

    # ============== Floating point types ==============
    assert rawConverter.convertType("float") == "float"
    assert rawConverter.convertType("double") == "float"
    assert rawConverter.convertType("float32_t") == "float"
    assert rawConverter.convertType("float64_t") == "float"
    assert rawConverter.convertType("float32") == "float"
    assert rawConverter.convertType("float64") == "float"

    # ============== Boolean types ==============
    assert rawConverter.convertType("bool") == "bool"

    # ============== String types ==============
    assert rawConverter.convertType("string") == "str"

    # ============== Void types ==============
    assert rawConverter.convertType("void") == "None"

    # ============== Any types ==============
    assert rawConverter.convertType("Any") == "Any"
    assert rawConverter.convertType("") == "Any"


def test_convert_type_with_pointer(rawConverter: TypeConverter):
    # ============== Integer types ==============
    assert rawConverter.convertType("int*") == "int"
    assert rawConverter.convertType("uint32_t*") == "int"
    assert rawConverter.convertType("uint64_t*") == "int"
    assert rawConverter.convertType("uint16_t*") == "int"
    assert rawConverter.convertType("uint8_t*") == "int"
    assert rawConverter.convertType("unsigned int*") == "int"
    assert rawConverter.convertType("unsigned long*") == "int"
    assert rawConverter.convertType("unsigned short*") == "int"

    # ============== Floating point types ==============
    assert rawConverter.convertType("float*") == "float"
    assert rawConverter.convertType("double*") == "float"
    assert rawConverter.convertType("float32_t*") == "float"
    assert rawConverter.convertType("float64_t*") == "float"

    # ============== Boolean types ==============
    assert rawConverter.convertType("bool*") == "bool"
    assert rawConverter.convertType("string*") == "str"
    assert rawConverter.convertType("void*") == "None"
    assert rawConverter.convertType("Any*") == "Any"


def test_convert_type_with_reference(rawConverter: TypeConverter):
    # ============== Integer types ==============
    assert rawConverter.convertType("const int&") == "int"
    assert rawConverter.convertType("const uint32_t&") == "int"
    assert rawConverter.convertType("const uint64_t&") == "int"
    assert rawConverter.convertType("const uint16_t&") == "int"
    assert rawConverter.convertType("const uint8_t&") == "int"
    assert rawConverter.convertType("const unsigned int&") == "int"
    assert rawConverter.convertType("const unsigned long&") == "int"
    assert rawConverter.convertType("const unsigned short&") == "int"

    # ============== Floating point types ==============
    assert rawConverter.convertType("const float&") == "float"
    assert rawConverter.convertType("const double&") == "float"

    # ============== Boolean types ==============
    assert rawConverter.convertType("const bool&") == "bool"

    # ============== String types ==============
    assert rawConverter.convertType("const string&") == "str"

    # ============== Void types ==============
    assert rawConverter.convertType("const void&") == "None"

    # ============== Any types ==============
    assert rawConverter.convertType("const Any&") == "Any"


def test_registered_types(rawConverter: TypeConverter):
    rawConverter.addType("TestType", "TestType")

    assert rawConverter.convertType("TestType") == '"TestType"'
    assert rawConverter.convertType("TestType*") == '"TestType"'
    assert rawConverter.convertType("const ntt::TestType&") == '"TestType"'


def test_registered_test_type(rawConverter: TypeConverter):
    rawConverter.addType("TestType", "TestType")
    rawConverter.addType("TestType2", "TestType2")

    assert rawConverter.convertType("TestType") == '"TestType"'
    assert rawConverter.convertType("TestType2") == '"TestType2"'
    assert rawConverter.convertType("TestType*") == '"TestType"'
    assert rawConverter.convertType("TestType2*") == '"TestType2"'
    assert rawConverter.convertType("const ntt::TestType&") == '"TestType"'
