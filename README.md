# Installation\n
#000000  Install Python version 3.10.18 or create a virtual environment\n
#000000 Install PostgreSQL 16.1\n
#000000 Install Django 5.2.4 **pip install Django**\n
#000000 Run **pip install requirements.txt** inside this directory.\n\n

# Setup\n
#000000 Create a PostgreSQL user **sudo -u postgres createuser -s $USER**\n
#000000 Login to postgres using the new user **sudo -u postgres psql postgres**\n
#000000 Create database user and database, you can change it to your preferred user, password, and database name. Just make sure to change the settings.py file configuration for the database engine.\n
  **CREATE ROLE wingz LOGIN PASSWORD 'pass';
    CREATE DATABASE ride_app_db WITH OWNER = wingz;**\n
#000000 Stop the current running PostgreSQL service and run it in a Docker container to use PostGIS (this extension is for geographic point fields) and to make sure that you're using the exact port.\n
  **sudo docker run --name postgis   -e POSTGRES_USER=wingz   -e POSTGRES_PASSWORD=pass   -e POSTGRES_DB=ride_app_db   -p 5432:5432   -d postgis/postgis:16-3.4**\n
*Note: If you can install PostGIS on your device, it's okay; this step is for devices or current PostgreSQL versions that are not compatible with PostGIS. Or any problem installing PostGIS*\n
#000000 Migrate database **python manage.py makemigrations && python manage.py migrate** \n

# Usage\n
#000000 Run the project **python manage.py runserver**\n
#000000 Create a superuser as admin **python manage.py createsuperuser**
#000000 Login as superuser to get token as credentials for new request **curl -X POST http://127.0.0.1:8000/api-token-auth/   -H "Content-Type: application/json"   -d '{"username": "your_username_here", "password": "your_password"}'**
*Note: that only user with admin role is permitted to access API endpoints*
## Example CRUD
#000000 Creating New User
**curl -X POST http://127.0.0.1:8000/api/users/   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"   -d '{
        "email": "",
        "password": "",
        "first_name": "",
        "last_name": "",
        "phone_number": "",
        "role": "rider"
      }'**
      
#000000 Updating User
**curl -X PUT http://127.0.0.1:8000/api/users/{id}   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"   -d '{
        "email": "",
        "password": "",
        "first_name": "",
        "last_name": "",
        "phone_number": "",
        "role": "rider"
      }'**
      
#000000 List Users *Note: you can put ID to only get specific user*      
**curl -X GET http://127.0.0.1:8000/api/users/   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**

#000000 Delete User 
**curl -X DELETE http://127.0.0.1:8000/api/users/{id}   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**

Creating New Ride
**curl -X POST http://127.0.0.1:8000/api/rides/   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"   -d '{
    "status": "en-route",
    "id_rider": 1,
    "id_driver": 2,
    "pickup_latitude": 13.7749,
    "pickup_longtitude": -122.4194,
    "dropoff_latitude": 37.8044,
    "dropoff_longtitude": -122.2711,
    "pickup_time": "2025-08-03T14:30:00Z"
      }'**
      
## Sorting endpoints 
*sorting value: asc for ascending,desc for descending*

#000000 Sorting using Pickup time
**curl -X GET http://127.0.0.1:8000/api/rides/?pickup_time=desc   -H "Content-Type: application/json"   -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**

#000000 Sorting using nearest pickup location based on inputted position(longtitude,latitude)
**curl -X GET "http://127.0.0.1:8000/api/rides/?lat=37.7749&lng=-122.4194" -H "Content-Type: application/json" -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**

#000000 Sorting using asc or desc pickup location
**curl -X GET "http://127.0.0.1:8000/api/rides/?lat=37.7749&lng=-122.4194&distance=desc" -H "Content-Type: application/json" -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**

#000000 Sorting using both pickup time and pickup location
**curl -X GET "http://127.0.0.1:8000/api/rides/?lat=37.7749&lng=-122.4194&distance=desc&pickup_time=asc" -H "Content-Type: application/json" -H "Authorization: Token This_is_a_sample_token_7da01819b088b7be9a8b46b4b0e4b307421d8300"**


