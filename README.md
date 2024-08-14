# OpenAI Function Calling with cal.com API Chatbot

## Overview

This repository contains a Python-based interactive chatbot built using OpenAI's function calling capabilities. The chatbot enables users to interact with their cal.com account through a chat interface, allowing them to book, list, and cancel events using the cal.com API. The application provides a simple, user-friendly interface to manage events directly from a chat interface.

## Features

- **Book a New Event:** The chatbot guides the user through the process of booking a new event, collecting necessary details like date, time, and reason before confirming the booking.
- **List Scheduled Events:** Users can retrieve a list of their scheduled events by simply asking the chatbot, which fetches events based on the user's email.
- **Cancel an Event:** Users can cancel specific events by providing the time of the event they wish to cancel.
- **Interactive Web Interface:** The application includes a basic web interface, allowing users to interact with the chatbot through a web page.

## Tech Stack

- **Python:** The main programming language used for building the chatbot logic.
- **Flask:** A micro web framework used to handle the web server and API routing.
- **OpenAI API:** Utilized for integrating OpenAI's function calling capabilities, enabling intelligent responses and function invocation.
- **cal.com API:** Used for event management, including creating, listing, and canceling events.
- **HTML:** A simple HTML template (`chat.html`) is used to create the web interface.

## Folder Structure

- `templates/chat.html`: The HTML template for the web interface of the chatbot.
- `api_key.json`: A JSON file containing API keys for cal.com and OpenAI.
- `app.py`: The main Python script that implements the chatbot functionality using Flask and handles API interactions.
- `requirements.txt`: Lists all the dependencies required to run the project.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git

2. **Navigate to the Project Directory:**

    ```bash
    cd your-repo-name
    ```

3. **Create a Virtual Environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # For Windows: .\env\Scripts\activate
    ```

4. **Install the Required Packages:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Add API Keys:**
    - Add your cal.com and OpenAI API keys to the `api_key.json` file as shown below:

    ```json
    {
      "cal_api_key": "your_cal.com_admin_api_key",
      "openai_api_key": "your_openai_api_key"
    }
    ```

## Running the Application

1. **Start the Flask Server:**

    ```bash
    python app.py
    ```

2. **Access the Web Interface:**
    - Open your web browser and navigate to `http://127.0.0.1:5000/` to interact with the chatbot.

## API Endpoints

- **`GET /`:** Displays the chat interface.
- **`POST /chat`:** Handles user input and processes chatbot responses, including event creation, listing, and cancellation.

## Usage

- **Booking an Event:** Type something like "help me to book a meeting" and follow the chatbot's prompts.
- **Listing Events:** Ask "show me the scheduled events," and the chatbot will retrieve your events.
- **Canceling an Event:** Say something like "cancel my event at 3pm today," and the chatbot will find and cancel the event.

## Resources

- [OpenAI Function Calling Documentation](https://platform.openai.com/docs/guides/function-calling)
- [cal.com Booking API Documentation](https://cal.com/docs/enterprise-features/api/api-reference/bookings#find-all-bookings)
- [cal.com Slot API Documentation](https://cal.com/docs/enterprise-features/api/api-reference/slots#get-user-or-team-event-type-slots)
- [Generate OpenAI API Key](https://platform.openai.com/account/api-keys)
- [Create cal.com API Key](https://cal.com/docs/enterprise-features/api/authentication)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
