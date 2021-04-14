import pytest


def test_fail_no_markers():
    """
    test an assertion False with no markers on the test
    """
    assert False


def test_pass_no_markers():
    """
    test an assertion True with no markers on the test
    """
    assert True


@pytest.mark.unit
def test_pass_no_meta_marker():
    """
    test an assertion True with no meta marker BUT other marker present
    """
    assert True


@pytest.mark.unit
def test_fail_no_meta_marker():
    """
    test an assertion False with no meta marker BUT other marker present
    """
    assert False


@pytest.mark.unit
@pytest.mark.meta
def test_pass_empty_meta_marker():
    """
    test an assertion True with no kwargs in meta marker
    """
    assert True


@pytest.mark.unit
@pytest.mark.meta
def test_fail_empty_meta_marker():
    """
    test an assertion False with no kwargs in meta marker
    """
    assert False


@pytest.mark.unit
@pytest.mark.meta("positional")
def test_pass_positional_arg_meta_marker():
    """
    test an assertion True with no kwargs BUT positional in meta marker
    """
    assert True


@pytest.mark.unit
@pytest.mark.meta("positional")
def test_fail_positional_arg_meta_marker():
    """
    test an assertion False with no kwargs BUT positional in meta marker
    """
    assert False
