from prefect.testing.utilities import prefect_test_harness

from hello_ford import MessageEnum, get_bathing_water_quality_flow

AREA_ID = "ukk3101-26570"

def test_get_bathing_water_quality_flow():
    with prefect_test_harness():
        # run the flow against a temporary testing database
        assert get_bathing_water_quality_flow(AREA_ID) == MessageEnum.SAFE_INCIDENT.value
