# Omni Test

#### Environment Variables (Pre-requisites to run the project)
* Default environment variables will be maintained in `_env` file.
* Copy `_env` to `.env` (Try `cp -n _env .env || true`)

#### Project Run Instructions:
* Open Terminal
* Go to project directory
* Type `docker-compose -f local.yml up --build` for development. Append the args `-d` to have the docker build and run the project in the background

#### Accessing Project Shell
* Type `docker-compose -f local.yml exec <docker_compose_service_name> bash`. I.E: `docker-compose -f local.yml exec web bash`
* Pass the argument --user=root to access project shell as root user to install requirement dependencies. I.E: `docker-compose -f local.yml exec --user=root web bash`

#### Running Datafeeder Commands
* Restaurant, Restaurant Timeslots and Menu:  `docker-compose -f local.yml exec web bash -c "python manage.py restaurant_datafeeder"`
* User and User Purchase History:  `docker-compose -f local.yml exec web bash -c "python manage.py user_datafeeder"`

#### Running Pytest(Test Suit) with Coverage
* `docker-compose -f local.yml exec web bash -c "pytest"`

