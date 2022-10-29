from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule

from hello_ford import get_bathing_water_quality_flow

deployment = Deployment.build_from_flow(
    flow=get_bathing_water_quality_flow,
    name="bathing-water-quality",
    parameters={"area_id": "ukk3101-26570"},
    infra_overrides={"env": {"PREFECT_LOGGING_LEVEL": "DEBUG"}},
    work_queue_name="test",
    schedule=(CronSchedule(cron="0 6 * * *"))
)

if __name__ == "__main__":
    deployment.apply()
