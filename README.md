# Hello Prefect 2

Creating workflows using [Prefect 2](https://www.prefect.io/)

With a flow for a simple assessment of bathing water quality using the Environment Agency API
[Environment Agency Bathing Water API](https://environment.data.gov.uk/bwq/doc/api-reference-v0.6.html)

# Example response for a bathing water area
[https://environment.data.gov.uk/id/bathing-water/ukk3101-26570.json](https://environment.data.gov.uk/id/bathing-water/ukk3101-26570.json)

## Start the Prefect Orion Server locally
`prefect orion start`
By default this runs at [http://127.0.0.1:4200](http://127.0.0.1:4200)

## Scripts
`hello_ford.py` contains the flow and tasks
`deployment.py` uses Python to deploy the flow to the interface

## Run the deployment locally using the CLI
`prefect deployment run get-bathing-water-quality/bathing-water-quality`
`prefect agent start -q test`

## Sample input area ids
ukc2102-03600
ukc2102-03800
