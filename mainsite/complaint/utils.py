import os
import requests
def send_trackid(trackid, phone_number):
    try:
        print("send_trackid",trackid, phone_number) 
        # Vonage (or custom SMS provider) API credentials
        userid = os.getenv('USERID')
        sender = os.getenv('SENDER')
        api_key = os.getenv('API_KEY')
        track_template_id = os.getenv("TRACK_TEMPLATE_ID")

        # Message to send
        message_body = (f"""Dear Customer, your complaint id {trackid} has been registered. Please track the complaint post the two days for the resolution. Regards-The Sirsa central Coop Bank Ltd.""")
        
        # API URL
        url = 'https://www.proactivesms.in/sendsms.jsp'

        # Payload for the API request
        payload = {
            'user': userid,
            'password': api_key,
            'senderid': sender,
            'mobiles': phone_number,
            'sms': message_body,
            'tempid': track_template_id
        }

        # Make the API request
        response = requests.post(url, data=payload)
        print("response",response)
        return response
    except Exception as e:
        print("Error sending SMS:", str(e))
       