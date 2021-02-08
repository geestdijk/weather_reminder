This weather reminder project is being done to gain some skills in JWT Auth and Celery,
together with DRF and some JS.

I've also tried to practice some JS,
despite of no usage of any frontend framework.
The access token is stored in the memory and the refresh token is stored in the cookies.

An user can add or remove the email subscription for the weather updates.
It's done using PeriodicTasks and CrontabSchedular from the django-celery-beat at the backend.
The weather forecast data is also updated by Celery task from the third-party API.

Next steps are covering code by tests, linting and preparing the project for a deployment.
