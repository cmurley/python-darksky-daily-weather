# Daily Weather
# Get weather forcast from DarkSky API and send a notification

# https://github.com/Detrous/darksky
# https://github.com/Detrous/darksky/blob/master/darksky/forecast.py

# Goals:
# Get Daily forecast
# Get High Temp for the day and report on what to wear
# Report if I need an umbrella
# Report the current temperature if I need to remote start the car

def get_weather():
    from darksky.api import DarkSky
    from darksky.types import languages, units, weather

    darksky = DarkSky('yourDarkSkyApiKey')
    latitude = 'yourLat'
    longitude = 'yourLong'

    forecast = darksky.get_forecast(
        latitude, longitude
    )
    return forecast

# forecast.daily.data[0].
# summary
# precip_probability
# precip_type
# temperature_high
# temperature_low

# forcast.currently.apparent_temperature

class forecast_logic(object):
    def do_i_need_umbrella(precip_pct):
        # We want to ignore anything less than 10%
        if precip_pct <= 0.30:
            return False
        else:
            return True

    def what_to_wear(high_temp):
        if high_temp <= 40:
            return 'Dress warm.'
        elif high_temp > 40 and high_temp <= 60:
            return 'Definitley need a light jacket. Shorts are NOT an option.'
        elif high_temp > 60 and high_temp <= 74:
            return 'Bring a jacket or sweater just in case.'
        elif high_temp > 74:
            return 'It is T-Shirt weather today.'
    
    def is_it_cold (curr_temp):
        if curr_temp <= 45:
            return 'It\'s probably a good idea to remote start the car before you leave. #firstworldproblems'
        else:
            return ''

def build_notification():
    # Get Forecast
    weather = get_weather()
    daily_forecast = weather.daily.data[0]
    curr_temp = weather.currently.apparent_temperature

    umbrella = forecast_logic.do_i_need_umbrella(daily_forecast.precip_probability)
    clothes = forecast_logic.what_to_wear(daily_forecast.temperature_high)
    cold = forecast_logic.is_it_cold(curr_temp)

    temp_string = 'Right now it\'s {} degrees.\nThe high today is {} degrees with a low of {} degrees.'.format(
        str(round(curr_temp)),
        str(round(daily_forecast.temperature_high)),
        str(round(daily_forecast.temperature_low))
        )
    precip_string = 'There is a {} percent chance of {}. Bring an umbrella.'.format(
        str(daily_forecast.precip_probability*100),
        daily_forecast.precip_type
    ) 
    message = '*Todays Forecast*\n{} {}\n{}\n{}'.format(
        temp_string,
        clothes,
        daily_forecast.summary,
        cold)
    if umbrella == True:
        message += '\n{}\n'.format(precip_string)
    
    return message

#def send_webhook(message):
    #curl -X POST -H "Content-Type: application/json" -d '{"value1":"1"}' https://maker.ifttt.com/trigger/daily_weather/with/key/yourIFTTTAPIKey
    #import requests

    #api_key = 'yourIFTTTAPIKey'
    #trigger_name = 'daily_weather'

    #webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'.format(
    #    trigger_name,
    #    api_key
    #)

    #r = requests.post(webhook_url, data = {'value1':message})

# Post to a Slack channel
def send_message_to_slack(text):
    from urllib import request, parse
    import json

    post = {"text": "{0}".format(text)}

    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/your/slackWebhook",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

def main():
    todays_message = build_notification()
    #send_webhook(todays_message)
    send_message_to_slack(todays_message)

main()