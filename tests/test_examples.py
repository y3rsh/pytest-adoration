import logging
import pytest
from src.zippopotam.zipcode import ZipCode

valid_zip_codes = ["66046", "66502", "94608", "02861", "65202", "99705"]

logger = logging.getLogger(__name__)


@pytest.mark.meta(test_type="general", attack="happy path")
@pytest.mark.parametrize("zip_code", valid_zip_codes)
def test_valid_zip_codes(zippopotam_client, zip_code):
    """
    provided valid zip code data, validate response code and data load.
    """
    response = zippopotam_client.get_us_by_zip(zip_code)
    logger.debug(f"response is {response.text}")
    zip_data = ZipCode()
    zip_data.safe_load(response.text)
    assert response.status_code == 200
    assert zip_data.post_code == zip_code


id_named_valid_zip_codes = [
    # nodeid becomes tests/test_examples.py::test_valid_zip_codes_better_name[validzip66046]
    pytest.param("66046", id="validzip66046"),
    pytest.param("hgjfhg", marks=[pytest.mark.xfail], id="xfailed_example"),
    pytest.param("66502", marks=[pytest.mark.xfail], id="xpassed_example"),
    pytest.param("66502", marks=[pytest.mark.skip], id="skip_example"),
]


@pytest.mark.meta(test_type="general", attack="happy path")
@pytest.mark.parametrize("zip_code", id_named_valid_zip_codes)
def test_valid_zip_codes_better_name(zippopotam_client, zip_code):
    """
    same as valid test but show how to name each test iteration
    """
    response = zippopotam_client.get_us_by_zip(zip_code)
    logger.debug(f"response is {response.text}")
    zip_data = ZipCode()
    zip_data.safe_load(response.text)
    assert response.status_code == 200
    assert zip_data.post_code == zip_code
