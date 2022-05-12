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

#### API Documentations

## (1) List all restaurants that are open at a certain datetime
`{server_url}/api/restaurants/?datetime={}`

* If there is no `datetime` parameter provided the default value will be current datetime.

* Sample datetime iso string:
`2022-05-12T20:44:39.672091`

* Sample url:
`http://0.0.0.0:8080/api/restaurants/?datetime=2022-05-12T20:44:39.672091`


## (2) List top y restaurants that have more or less than x number of dishes within a price range, ranked alphabetically. More or less (than x) is a parameter that the API allows the consumer to enter.
``
`{server_url}/api/restaurants/menus/?min_no_menu={}&max_no_menu={}&min_price={}&max_price={}`

* `min_no_menu` minimum number of menu.
* `max_no_menu` maximum number of menu.
* `min_price` minimum price of menu.
* `max_no_menu` maximum number of menu.

* Sample url:
`http://0.0.0.0:8000/api/restaurants/menus/?min_no_menu=9&max_no_menu=11&min_price=14&max_price=100`

## (3) Search by Restaurant Name or Menu Name
`{server_url}/api/restaurants/menus/?search={name}`

* `{name}` can be any restaurant-name or menu-name

* Sample url:
`http://0.0.0.0:8080/api/restaurants/menus/?search=Hollandaise`


