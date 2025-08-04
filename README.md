# Installation<br>
*  Install Python version 3.10.18 or create a virtual environment<br>
* Install PostgreSQL 16.1<br>
* Install Django 5.2.4 **pip install Django**<br>
* Run **pip install requirements.txt** inside this directory.<br><br>

# Setup<br>
* Create a PostgreSQL user **sudo -u postgres createuser -s $USER**<br>
* Login to postgres using the new user **sudo -u postgres psql postgres**<br>
* Create database user and database, you can change it to your preferred user, password, and database name. Just make sure to change the settings.py file configuration for the database engine.<br>
  **CREATE ROLE wingz LOGIN PASSWORD 'pass';
    CREATE DATABASE ride_app_db WITH OWNER = wingz;**<br>
* Stop the current running PostgreSQL service and run it in a Docker container to use PostGIS (this extension is for geographic point fields) and to make sure that you're using the exact port.<br>
  **sudo docker run --name postgis   -e POSTGRES_USER=wingz   -e POSTGRES_PASSWORD=pass   -e POSTGRES_DB=ride_app_db   -p 5432:5432   -d postgis/postgis:16-3.4**<br>
*Note: If you can install PostGIS on your device, it's okay; this step is for devices or current PostgreSQL versions that are not compatible with PostGIS. Or any problem installing PostGIS*<br>
* Migrate database **python manage.py makemigrations && python manage.py migrate** <br>

# Usage<br>
* Run the project **python manage.py runserver**<br>
* Create a superuser as admin **python manage.py createsuperuser**<br>
* Login as superuser to get token as credentials for new request **curl -X POST http://127.0.0.1:8000/api-token-auth/   -H "Content-Type: application/json"   -d '{"username": "your_username_here", "password": "your_password"}'**<br>
*Note: that only user with admin role is permitted to access API endpoints*<br>
## Example CRUD<br>
* Creating New User<br>
**curl -X POST http://127.0.0.1:8000/api/users/   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"   -d '{
        "email": "",
        "password": "",
        "first_name": "",
        "last_name": "",
        "phone_number": "",
        "role": "rider"
      }'**<br>
      
* Updating User<br>
**curl -X PUT http://127.0.0.1:8000/api/users/{id}   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"   -d '{
        "email": "",
        "password": "",
        "first_name": "",
        "last_name": "",
        "phone_number": "",
        "role": "rider"
      }'**<br>
      
* List Users *Note: you can put ID to only get specific user*  <br>    
**curl -X GET http://127.0.0.1:8000/api/users/   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**<br><br>

* Delete User <br>
**curl -X DELETE http://127.0.0.1:8000/api/users/{id}   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**<br><br>

Creating New Ride<br>
**curl -X POST http://127.0.0.1:8000/api/rides/   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"   -d '{
    "status": "en-route",
    "id_rider": 1,
    "id_driver": 2,
    "pickup_latitude": 13.7749,
    "pickup_longtitude": -122.4194,
    "dropoff_latitude": 37.8044,
    "dropoff_longtitude": -122.2711,
    "pickup_time": "2025-08-03T14:30:00Z"
      }'**<br><br>
      
## Sorting endpoints <br>
*sorting value: asc for ascending,desc for descending*<br><br>

* Sorting using Pickup time<br>
**curl -X GET http://127.0.0.1:8000/api/rides/?pickup_time=desc   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**<br><br>

* Sorting using nearest pickup location based on inputted position(longtitude,latitude)<br>
**curl -X GET "http://127.0.0.1:8000/api/rides/?lat=37.7749&lng=-122.4194" -H "Content-Type: application/json" -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**<br><br>

* Sorting using asc or desc pickup location distance from the given position<br>
**curl -X GET "http://127.0.0.1:8000/api/rides/?lat=37.7749&lng=-122.4194&distance=desc" -H "Content-Type: application/json" -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**<br><br>

* Sorting using both pickup time and pickup location distance from the given position<br>
**curl -X GET "http://127.0.0.1:8000/api/rides/?lat=37.7749&lng=-122.4194&distance=desc&pickup_time=asc" -H "Content-Type: application/json" -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**<br><br>

## 🧾 SQL Report: Trips (> 1 Hour) by Driver and Month

To find the number of rides that lasted more than 1 hour, grouped by driver and by month, use this raw SQL query:<br>

```
SELECT 
    TO_CHAR(r.pickup_time, 'YYYY-MM') AS Month,
    ride.id_driver As Driver,
    COUNT(*) AS "Trips > 1 hour"
FROM 
    ride_app_ride ride
JOIN 
    ride_app_ride_event pickup_event 
    ON ride.id_ride = pickup_event.id_ride_id 
    AND pickup_event.description = 'Status changed to pickup'
JOIN 
    ride_app_ride_event dropoff_event 
    ON ride.id_ride = dropoff_event.id_ride_id 
    AND dropoff_event.description = 'Status changed to dropoff'
WHERE 
    EXTRACT(EPOCH FROM (dropoff_event.created_at - pickup_event.created_at)) > 3600
GROUP BY 
    Month, Driver```
