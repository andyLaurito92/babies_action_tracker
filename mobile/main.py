from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window
import json
from datetime import datetime


class BabiesActionTracker(App):
    def build(self):
        self.icon = 'baby_icon.png'

        # Create a main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Create buttons
        sleep_button = Button(text='Sleep', on_press=lambda instance: self.call_api('http://192.168.1.32:5001/add_sleep_action', 'sleep'))
        eat_button = Button(text='Eat', on_press=lambda instance: self.call_api('http://192.168.1.32:5001/add_eat_action', 'eat'))
        poop_button = Button(text='Poop', on_press=lambda instance: self.call_api('http://192.168.1.32:5001/add_poop_action', 'poop'))
        diaperchange_button = Button(text='Diaper Change', on_press=lambda instance: self.call_api('http://192.168.1.32:5001/add_diaper_change_action', 'diaper_change'))
        bath_button = Button(text='Bath', on_press=lambda instance: self.call_api('http://192.168.1.32:5001/add_bath_action', 'bath'))

        # Add buttons to the layout
        layout.add_widget(sleep_button)
        layout.add_widget(eat_button)
        layout.add_widget(poop_button)
        layout.add_widget(diaperchange_button)
        layout.add_widget(bath_button)

        return layout

    def call_api(self, api_url, action):
        # Get the current time
        current_time = datetime.now()

        # Format the current time as HH:mm:ss
        time_of_action = current_time.strftime("%Y-%m-%dT%H:%M:%S")

        # Body of the request to send
        request_data = {'timestamp': time_of_action}

        # Make the UrlRequest with the correct Content-Type header
        headers = {'Content-Type': 'application/json'}

        # Make an asynchronous API request using UrlRequest
        UrlRequest(api_url, req_body=json.dumps(request_data), req_headers=headers, on_success=self.on_success, on_failure=self.on_failure, on_error=self.on_error)

    def on_success(self, req, result):
        print(f"API call successful. Response: {json.dumps(result)}")

    def on_failure(self, req, result):
        print(f"API call failed. Status code: {req.resp_status}. Result was: {json.dumps(result)}")

    def on_error(self, req, error):
        print(f"An error occurred during the API call: {error}")

if __name__ == '__main__':
    BabiesActionTracker().run()

