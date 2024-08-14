from flask import Flask, request, jsonify, render_template
import openai
import requests
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chat.html')

def get_api_key(file_path, key):
    with open(file_path, 'r') as file:
        data = json.load(file)
        api_key = data.get(key)
        return api_key


def create_booking(date, time, reason):
    print("Create create event")
    return f"Event Created for the given {date}, {time}, {reason}"
    booking_data = {
        "responses": {
            "email": "dinesha.vennapoosa@gmail.com",
            "name": "Abhi",
            "notes": "testing",
            "location": {
                "optionValue": "",
                "value": "integrations:daily"
            }
        },
        "description" : reason,
        "start": date+'T'+time,
        "eventTypeId": 879513,
        "timeZone": "America/Indianapolis",
        "language": "en",
        "metadata": {},
    }

    url = f'{CAL_API_BASE_URL}/bookings?apiKey={CAL_API_KEY}'
    print(url)
 
    response = requests.post(url, json=booking_data)
    return response
    if response.status_code == 200:
        return "Actual booking has been done"
    else:
        return "Dummy Booking has been done"

def list_events(email):
    print("List create event")
    return f"Listing Events for the email - {email}"
    url = f'{CAL_API_BASE_URL}/bookings?apiKey={CAL_API_KEY}'
    url = f"{CAL_API_BASE_URL}/schedules"
    params = {
        "email": email
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        events = response.json()
        return "\n".join([f"{event['title']} at {event['start']}" for event in events])
    else:
        return f"Failed to list events: {response.text}"

def cancel_event(email, time):
    # First, we need to find the event
    print("Cancel create event")
    return f"Cancelling Events for the {email} for the {time}"
    events = list_events(email)
    target_event = next((event for event in events if event['start'].endswith(f"T{time}:00Z")), None)
    
    if not target_event:
        return "No event found at the specified time"
    
    url = f"{CAL_API_BASE_URL}/schedules/{target_event['id']}"
    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        return "Event cancelled successfully"
    else:
        return f"Failed to cancel event: {response.text}"


# Define the function descriptions for OpenAI
functions = [
    {
        "name": "create_booking",
        "description": "Create a new booking in the calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date of the booking (YYYY-MM-DD)"},
                "time": {"type": "string", "description": "Time of the booking (HH:MM:SS)"},
                "reason": {"type": "string", "description": "Reason for the booking"}
            },
            "required": ["date", "time", "reason"]
        }
    },
    {
        "name": "list_events",
        "description": "List scheduled events for a user",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Email of the user"}
            }
        }
    },
    {
        "name": "cancel_event",
        "description": "Cancel an event for a user",
        "parameters": {
            "type": "object",
            "properties": {
                "time": {"type": "string", "description": "Time of the event to cancel (HH:MM)"}
            },
            "required": ["email", "time"]
        }
    }
]

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    user_input = request.json['message']
    conversation_history.append({"role": "user", "content": user_input})
    
    openai.api_key = OPENAI_API_KEY

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=conversation_history,
        functions=functions,
        function_call="auto"
    )
    
    # Process the response
    message = response["choices"][0]["message"]
    print(message.get("function_call"))
    print("Stage 1")
    
    if message.get("function_call"):
        print("Stage 2")
        function_name = message["function_call"]["name"]
        function_args = json.loads(message["function_call"]["arguments"])
        
        if function_name == "create_booking":
            # Check if we have all required information
            missing_info = [arg for arg in ["date", "time", "reason"] if arg not in function_args]
            
            if missing_info:
                # If information is missing, ask for it
                response_text = f"I need more information to book the meeting. Can you please provide the following: {', '.join(missing_info)}?"
                conversation_history.append({"role": "assistant", "content": response_text})
                return jsonify({"response": response_text})
            else:
                # If we have all information, create the event
                result = create_booking(function_args["date"], function_args["time"], function_args["reason"])
                conversation_history.append({"role": "assistant", "content": result})
                return jsonify({"response": result})
        if function_name == "list_events":
                function_args['email'] = 'user_email@gmail.com'
                result = list_events(function_args['email'])
                conversation_history.append({"role": "assistant", "content": result})
                return jsonify({"response": result})

        if function_name == "cancel_event":
            function_args['email'] = 'user_email@gmail.com'
            missing_info = [arg for arg in ["time"] if arg not in function_args]
            
            if missing_info:
                # If information is missing, ask for it
                response_text = f"I need more information to Cancel the event. Can you please provide the following: {', '.join(missing_info)}?"
                conversation_history.append({"role": "assistant", "content": response_text})
                return jsonify({"response": response_text})
            else:
                # If we have all information, create the event
                result = cancel_event(function_args["email"], function_args["time"])
                conversation_history.append({"role": "assistant", "content": result})
                return jsonify({"response": result})
        print("Stage 3")
    else:
        print("Stage 4")
        print("Listing is not executed")
        conversation_history.append({"role": "assistant", "content": message["content"]})
        return jsonify({"response": message["content"]})

if __name__ == '__main__':
    global conversation_history, OPENAI_API_KEY, CAL_API_KEY, CAL_API_BASE_URL
    conversation_history = []
    CAL_API_KEY = get_api_key('api_key.json', 'cal_api_key')
    OPENAI_API_KEY = get_api_key('api_key.json', 'openai_api_key')
    CAL_API_BASE_URL = "https://api.cal.com/v1"

    app.run(debug=True)