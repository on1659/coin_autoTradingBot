
import datetime

# Configure OAuth2 access token for authorization: strava_oauth
swagger_client.configuration.access_token = '4fedf5b7f13c26db633f44d16ed972e05eca3c9b'

# create an instance of the API class
api_instance = swagger_client.ActivitiesApi()
name = name_example # String | The name of the activity.
type = type_example # String | Type of activity. For example - Run, Ride etc.
startDateLocal =cur
elapsedTime = 56 # Integer | In seconds.
description = description_example # String | Description of the activity. (optional)
distance = 3.4 # Float | In meters. (optional)
trainer = 56 # Integer | Set to 1 to mark as a trainer activity. (optional)
commute = 56 # Integer | Set to 1 to mark as commute. (optional)

try: 
    # Create an Activity
    api_response = api_instance.createActivity(name, type, startDateLocal, elapsedTime, description=description, distance=distance, trainer=trainer, commute=commute)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->createActivity: %s\n" % e)
