# Omni Test

### Environment Variables (Pre-requisites to run the project)
* Default environment variables will be maintained in `_env` file.
* Copy `_env` to `.env` (Try `cp -n _env .env || true`)

### Project Run Instructions:
* Open Terminal
* Go to project directory
* Type `docker-compose -f local.yml up --build` for development. Append the args `-d` to have the docker build and run the project in the background

### Accessing Project Shell
* Type `docker-compose -f local.yml exec <docker_compose_service_name> bash`. I.E: `docker-compose -f local.yml exec web bash`
* Pass the argument --user=root to access project shell as root user to install requirement dependencies. I.E: `docker-compose -f local.yml exec --user=root web bash`

### Running Datafeeder Commands
* Restaurant, Restaurant Timeslots and Menu:  `docker-compose -f local.yml exec web bash -c "python manage.py restaurant_datafeeder"`
* User and User Purchase History:  `docker-compose -f local.yml exec web bash -c "python manage.py user_datafeeder"`

### Running Pytest(Test Suit) with Coverage
* `docker-compose -f local.yml exec web bash -c "pytest"`

## API Documentations

### (1) List all restaurants that are open at a certain datetime
`{server_url}/api/restaurants/?datetime={}`
* Request Type: `GET`

* If there is no `datetime` parameter provided the default value will be current datetime.

* Sample datetime iso string:
`2022-05-12T20:44:39.672091`

* Sample url:
`http://0.0.0.0:8080/api/restaurants/?datetime=2022-05-12T20:44:39.672091`


### (2) List top y restaurants that have more or less than x number of dishes within a price range, ranked alphabetically. More or less (than x) is a parameter that the API allows the consumer to enter.
``
`{server_url}/api/restaurants/menus/?total_menu_min={}&total_menu_max={}&price_min={}&price_max={}`
* Request Type: `GET`

* `total_menu_min` minimum number of menu.
* `total_menu_max` maximum number of menu.
* `price_min` minimum price of menu.
* `price_max` maximum price of menu.

* Sample url:
`http://0.0.0.0:8080/api/restaurants/menus/?total_menu_min=9&total_menu_max=10&price_min=10&price_max=11`


### (3) Search by Restaurant Name or Menu Name
`{server_url}/api/restaurants/menus/?search={name}`
* Request Type: `GET`

* `{name}` can be any restaurant-name or menu-name

* Sample url:
`http://0.0.0.0:8080/api/restaurants/menus/?search=coffee`


### (4) Process a user purchasing a dish from a restaurant, handling all relevant data changes in an atomic transaction. Do watch out for potential race conditions that can arise from concurrent transactions!
`{server_url}/api/users/orders/`
* Request Type: `POST`

* Data: 
```
{
    "user": {user.id},
    "menu": {menu.id}
}
```

* Sample url:
`http://0.0.0.0:8080/api/users/orders/` with data:

```
{
    "user": 0,
    "menu": 1
}
```
* Note: This is a bad approach because I am not checking wheather the request is authenticate or not. Best approach would be:

```
{
    "menu": 1
}
```
and the `user` will be fetched through the request (Auth/token), so that only user himself can place an order for himself. Since I am not implementing Auth, I created a dummy order API.
