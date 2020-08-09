# analytical_dashboard

## API Dodumentation

1. ### Departments and objectives analysis API
   **Method**: ***GET***

   **URL**: ***http://{IP}:{PORT}/dashboard/departments/?on_track_filter=2 weeks&recently_upd_filter=3 weeks***

   Response(success): 
   ```
   {"status": "OK", "data": {"objectives_on_track": {"date_since": "Friday 07/31",      "on_track": 1, "total": 3, "on_track_ratio": 33}, "objectives_updated_recently": {"date_since": "2 weeks", "update_ratio": 67, "change": 0,
    "percentage_change": 0.0, "direction": "up"}, "departments": [{"name": "Product", "teams_count": 2, "users_count": 2, "objectives_count": 1, "objectives_on_track_ratio": 0}, {"name": "Engineering", "teams_count": 1, "users_count": 1, "objectives_count": 2, "objectives_on_track_ratio": 50}, {"name": "Marketing", "teams_count": 0, "users_count": 0, "objectives_count": 0, "objectives_on_track_ratio": "--"}]}}
    ```

    `objectives_on_track` has the on track objectives since `date_since` and the `on_track_ratio`

    `objectives_updated_recently` has the ratio of updated_objectives to the total objectives in `date_since`, also change in objectives update count since last week.

    `departments` has the name, teams count, users count, total no of objectives and the
    objectives on track ratio of all the departments. 

    Response(error):

    ```
    {"status":"error", "data": "<error message>"}
    ```

    > Note: Default on_track_filter value is `1 weeks` and recently_upd_filter is `2 weeks`

2. ### Teams analysis API
    **Method**: ***GET***

    **URL**: ***http://{IP}:{PORT}/dashboard/teams/?department_name=product***

    Response(success)

    ```
    {"status": "OK", "data": {"teams": [{"team_leader": "Kailash", "members": []}]}}
    ```

    Response(error)

    ```
    {"status":"error", "data": "<error message>"}
    ```

#### [Schema diagram](https://dbdiagram.io/d/5f2ce3e908c7880b65c569e7)

## Deployment steps
### Prerequisites
1. Create postgres user

   ```
   create user postgres_user with encrypted password 'pg123';
   ```

2. Create postgres dev and prod databases

   ```
   create database dashboard;
   create database dashboard_prod;
   ```
3. Alter user to give create database role

   ```
   alter user postgres_user CREATEDB;
   grant all privileges on database dashboard to postgres_user;
   grant all privileges on database dashboard to postgres_user;
   ```

4. Change the settings.dev and settings.prod database details

### Local deployment

Go to the project directory

#### Install the dependancies

```
python -m pip install -r requirements.txt
```
#### Set environment variable(for production deployment)
##### For windows
```
set ENV=PROD
```
##### For non windows
```
export ENV=PROD
```
#### Run migration
```
python manage.py migrate
```
#### Create the server
```
python manage.py runserver 0.0.0.0:{PORT}
```

> Note: Set the environment variable for only for production deployment; Default is: `dev`

### Docker deployment

#### Build the image
##### PROD
```
docker build -t dashboard --build-arg DB_ENV=prod .
```
##### DEV
```
docker build -t dashboard .
```

#### Run the image
```
docker run -d dashboard -p {PORT}:8000 -v {LOG_DIR}:/usr/app/src/analytical_dashboard/logs dashboard
```

### Run tests
```
python manage.py test
```

#### Known bugs and Limitations
* Not enough debug logging
* Negative testcases were not implemented

#### What has been completed
The basic analytical dashboard APIs are done. Yet there's a room for accomodating many analytical entities.
If more time was given, would have added more analytics for other entities like users, teams etc
