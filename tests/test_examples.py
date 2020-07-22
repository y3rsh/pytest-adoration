import pytest
import logging
from zip import Zip

valid_zip_codes = ["66046", "66502", "94608", "02861", "65202", "99705"]

logger = logging.getLogger(__name__)


@pytest.mark.integration
@pytest.mark.parametrize("zip", valid_zip_codes)
def test_valid_zip_codes(zippopotam_client, zip):
    response = zippopotam_client.get_us_by_zip(zip)
    logger.debug(f"response is {response.text}")
    zip_data = Zip()
    zip_data.safe_load(response.text)
    assert response.status_code == 200
    assert zip_data.post_code == zip
