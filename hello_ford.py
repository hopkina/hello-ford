import sys
from datetime import datetime
from enum import Enum
from typing import Tuple, TypedDict

import requests
from prefect import flow, get_run_logger, task


class MessageEnum(Enum):
    SAFE_QUALITY = "Safe to swim - excellent quality"
    UNSAFE_QUALITY = "Not safe to swim - general quality"
    SAFE_INCIDENT = "Safe to swim - incident passed"
    UNSAFE_INCIDENT = "Not safe to swim - outstanding incident"


@task(name="get-bathing-water-area-information", 
      description="Get information for a bathing area",
      retries=3, 
      retry_delay_seconds=10)
def call_bathing_water_api(area_id: str) -> TypedDict:

    logger = get_run_logger()

    url = f"https://environment.data.gov.uk/id/bathing-water/{area_id}.json"
    response = requests.get(url)

    status_code = response.status_code
    logger.info(f"Response status: {status_code}")

    if not status_code == 200:
        raise ValueError(f"Request from {url} unsucessful")
    else:
        return response.json()

@task(name="parse-response", 
      description="Parse bathing water reponse",
      tags=["tutorial","tag-test"])
def parse_bwq(response: TypedDict) -> Tuple[str, str]:

    logger = get_run_logger()

    primary_topic = response['result']['primaryTopic']
    assessment_value = primary_topic['latestComplianceAssessment']['complianceClassification']['name']['_value']
    if "latestOpenIncident" in primary_topic:
        end_latest_incident = primary_topic['latestOpenIncident']['expectedEndOfIncident']['_value']
    else:
        end_latest_incident = None

    logger.info(f"Assessment value: {assessment_value}")
    logger.info(f"Expected end of latest incident: {end_latest_incident}")

    return assessment_value, end_latest_incident

@task(name="safe-to-swim", 
      description="Use response value to assess if safe to swim",
      tags=["tutorial","tag-test"])
def safe_to_swim(assessment_value: str, end_latest_incident: str) -> str:

    if assessment_value == 'Excellent':
        if end_latest_incident is not None:
            now = datetime.now()
            latest = datetime.strptime(end_latest_incident, "%Y-%m-%d")
            if latest.date() < now.date():
                return MessageEnum.SAFE_INCIDENT.value
            else:
                return MessageEnum.UNSAFE_INCIDENT.value
        else:
            return MessageEnum.SAFE_QUALITY.value
    else:
        return MessageEnum.UNSAFE_QUALITY.value


@flow(name="get-bathing-water-quality", 
      description="Flow to get bathing water quality from the EA bathing water api",
      version="v_00")
def get_bathing_water_quality_flow(area_id: str):
    # run tasks and subflows
    logger = get_run_logger()
    logger.info(f"Area ID: {area_id}")

    bwq_json = call_bathing_water_api(area_id)
    assessment_value, end_latest_incident = parse_bwq(bwq_json)
    message = safe_to_swim(assessment_value, end_latest_incident)
    
    logger.info(f"Result: {message}")

    return message


if __name__ == "__main__":

    # example value
    # "ukk3101-26570"
    area_id = sys.argv[1]
    message = get_bathing_water_quality_flow(area_id)
