from unittest import mock

import pytest

from scrappy.scrappers import rpp


@mock.patch.object(rpp, 'WebServer')
def test_run_raises_type_error_on_bad_date(WebServer):
    logger = mock.Mock()
    scrapper = rpp.RPP(logger)

    with pytest.raises(TypeError):
        scrapper.run(date="11-11-11")
        scrapper.run(date="11-11-111")
        scrapper.run(date="1111-111-11")
