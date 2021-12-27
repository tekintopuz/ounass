# Ounass Django-React-Nginx-Postgres-Docker
A Docker Compose ounass with Nginx, Django, Gunicorn, React and Postgres database.
The Postgres data is saved locally in the `postgres` directory, and any changes saved to the database while the app is running will persist.  
Static and media files are configured to be served by Nginx, and stored locally in the `backend\static` and `backend\media` directories.

## Nginx configuration
The default Nginx configuration file can be found at `nginx/nginx.conf`.  
It's set to run the site for local development at `http://localhost` or `http://127.0.0.1` with default http port 80

## Postgres configuration
Default Postgres setting can be found in `.env`. The Postgres Docker image will automatically create a database with these settings when the container is started.
`postgresql` everywhere for default values and used in  `backend\ounass\settings.py` and matched the container name in the `docker-compose.yml` file for the Postgres container.

    POSTGRES_DB=ounass
    POSTGRES_USER=ounass
    POSTGRES_PASSWORD=ounass1234
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432

## Backend Django Api In 8000 Port
   ```json
   [
	{
		"name": "Create A Campaign",
		"request": {
			"auth": {
				"type": "noauth"
			},
			"method": "POST",
			"header": [
				{
					"key": "Content-Type",
					"value": "application/json",
					"type": "text"
				}
			],
			"body": {
				"mode": "raw",
				"raw": {"name":"User Custom Name [Tekin TOPUZ]"},
				"options": {
					"raw": {
						"language": "json"
					}
				}
			},
			"url": {
				"raw": "http://127.0.0.1:8000/api/v1/campaigns/",
				"protocol": "http",
				"host": [
					"127",
					"0",
					"0",
					"1"
				],
				"port": "8000",
				"path": [
					"api",
					"v1",
					"campaigns",
					""
				]
			}
		},
		"response": []
	},
	{
		"name": "Create An Adset API",
		"request": {
			"method": "POST",
			"header": [],
			"url": {
				"raw": "http://localhost:8000/api/v1/addsets/",
				"protocol": "http",
				"host": [
					"localhost"
				],
				"port": "8000",
				"path": [
					"api",
					"v1",
					"addsets",
					""
				]
			}
		},
		"response": []
	},
	{
		"name": "AdSetInsightAPI",
		"request": {
			"method": "GET",
			"header": [],
			"url": {
				"raw": "http://localhost:8000/api/v1/insight/<ad_set_id>(sample=120330000091604509)",
				"protocol": "http",
				"host": [
					"localhost"
				],
				"port": "8000",
				"path": [
					"api",
					"v1",
					"insight",
					"120330000091604509"
				]
			}
		},
		"response": []
	},
	{
		"name": "CreativePreviewApi",
		"request": {
			"method": "GET",
			"header": [],
			"url": {
				"raw": "http://localhost:8000/api/v1/previews/<creative_id>(sample=120330000091642509)",
				"protocol": "http",
				"host": [
					"localhost"
				],
				"port": "8000",
				"path": [
					"api",
					"v1",
					"previews",
					"120330000091642509"
				]
			}
		},
		"response": []
	},
	{
		"name": "Create Ad Creative API",
		"request": {
			"method": "POST",
			"header": [],
			"url": {
				"raw": "http://localhost:8000/api/v1/adcreative/",
				"protocol": "http",
				"host": [
					"localhost"
				],
				"port": "8000",
				"path": [
					"api",
					"v1",
					"adcreative",
					""
				]
			}
		},
		"response": []
	}
]

   ```

## Frontend React In 3000 Port


## Install Instructions
Prerequisite: You need to have Docker installed on the system where you'll be running this app. [Get Docker](https://docs.docker.com/install/)


1. Using your command line interface, `cd` to the cloned directory containing the docker-compose.yml file.
2. Build the images and run the containers:
    ```sh
    $ docker-compose up -d --build
    ```
3. To stop the application, run `docker-compose down`    


