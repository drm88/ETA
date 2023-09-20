import googlemaps
from datetime import datetime, timedelta
from twilio.rest import Client

def get_commute_duration():
    #Set Home and Work locations
    home_address = '$HOME_ADDRESS'
    work_address = '$WORK_ADDRESS'

    #Configure Google Maps API client
    gmaps_api_key = '$GOOGLE_MAPS_API_KEY'
    gmaps = googlemaps.Client(key=gmaps_api_key)

    #Get directions
    directions = gmaps.directions(home_address, work_address)
    
    #Figure out duration of the commute, {duration} is a formatted string {duration_seconds} is the time in seconds
    duration = directions[0]['legs'][0]['duration']['text']
    duration_seconds = directions[0]['legs'][0]['duration']['value']
    return duration, duration_seconds

def send_twilio_message(message):
    # Set up Twilio client
    twilio_account_sid = '$TWILIO_ACCOUNT_SID'
    twilio_auth_token = '$TWILIO_AUTH_TOKEN'
    twilio_phone_number = '$TWILIO_NUMBER'
    your_phone_number = '$YOUR_NUMBER'
    client = Client(twilio_account_sid, twilio_auth_token)

    client.messages.create(
        to=your_phone_number,
        from_=twilio_phone_number,
        body=message
    )

def main():
    duration = get_commute_duration()[0]
    duration_seconds = get_commute_duration()[1]

    now = datetime.now()
    arrival_time = (now + timedelta(seconds= duration_seconds)).strftime('%I:%M %p')

    message = (
        f"Estimate time to work at is {duration}. \n\n"
        f"Leave now to arrive at approximatley {arrival_time}\n"
    )

    send_twilio_message(message)

if __name__ == "__main__":
    main()