from pytest import raises

from rippler import Rippler, RipplesException, RipplesResponse
from rippler.main import api_endpoint, stringify


class TestMisc:

    def test_stringify(self):
        _in = {"foo": True, "bar": False, "baz": [True, False]}
        _out = {"foo": "true", "bar": "false", "baz": ["true", "false"]}

        assert stringify(_in) == _out

    def test_api_endpoint(self):
        assert api_endpoint(
            "foo/", "bar/") == "https://webapp.drinkripples.com/api/v1/foo/bar"


class TestRipplesResponse:

    def test_unexpected_format(self):
        payload = {"foo": 123}
        with raises(RipplesException, match="Unexpected API response"):
            RipplesResponse(payload)

    def test_error(self):
        payload = {"data": 123, "err": "some error!"}
        with raises(RipplesException, match="Error in API response"):
            RipplesResponse(payload)

    def test_no_error(self):
        payload = {"data": 123, "err": None}
        assert RipplesResponse(payload).data == 123


class TestRippler:
    # Note: only test what doesn't send actual images to machines

    def test_locations(self):
        # The Empire State Building
        lat = 40.74880
        lon = 73.98559

        response = Rippler.locations(lat, lon)
        assert isinstance(response['locations'], list)

    def test_upload_service_config(self):
        # The Plaza Hotel in NYC
        location_id = "624c3184722ae5b15a3a8cb0"

        ripple = Rippler(location_id=location_id)
        response = ripple._upload_service_config()
        assert isinstance(response['url'], str)
        assert isinstance(response['params'], dict)
