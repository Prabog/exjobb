# Imported Modules
import requests

# Documentation at: https://pushover.net/api

class PushoverNotification:
    def __init__(self, user_key, api_token):
        self.user = user_key
        self.token = api_token
        self.api_url = "https://api.pushover.net/1/messages.json"

    def send_msg(self, message):
        data = {
            "token": self.token, # Required
            "user": self.user, # Required
            "message": message, # Required
            "sound": "vibrate" # optional, a list of sound is in the documentation
        }

        # POST an HTTPS request to Pushover API with the data.
        requests.post(self.api_url, data=data)
        print("Message sent.")

if __name__ == "__main__":
    # Required information; gathered from Pushover site.
    user_key = "utcd12k537bsjcax6w2i71exe4t39t"
    api_token = "ars2yhwu4euahs33hsyqj7j9bzy8td"

    notifier = PushoverNotification(user_key, api_token)
    message = "Ditt kaffe börjar bli kallt."

    notifier.send_msg(message)
