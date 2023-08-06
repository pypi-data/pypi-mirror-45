from astep_form_utils import FieldSet, StringField


def test_validate_positive():
    field_set = FieldSet(
        StringField("test")
    )
    assert field_set.is_valid({"test": "foo"})


def test_validate_negative():
    field_set = FieldSet(
        StringField("test")
    )
    assert not field_set.is_valid({"test": 1})
