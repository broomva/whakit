# WhaKit - WhatsApp Chatbot Framework

WhaKit provides a comprehensive implementation of a WhatsApp chatbot using Python. It includes all the methods needed to create a sample bot with various functionalities, such as handling messages, integrating with AI services, managing conversation state, and interacting with external services like Google Sheets.

## Features

- **FastAPI** for handling webhook requests.
- **LangChain** for AI integrations.
- **AsyncIO** for asynchronous operations.
- **WhatsApp Cloud API** integration.
- **Google Sheets API** for data storage.
- **Modular Design** for scalability and extensibility.
- **Customizable Conversation Flows** including appointment scheduling and assistant queries.
- **Error Handling and Logging** using Python's `logging` module.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/whakit.git
cd whakit

2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:
pip install -r requirements.txt

4 Set up environment variables:
Create a .env file in the root directory and add the necessary environment variables as shown in .env.example.

5 Run the application:
uvicorn whakit.main:app --reload


## Configuration

Update the settings.py file or the .env file with your configuration settings. You can customize the AI assistant’s behavior, greetings, menu options, and more.

## Usage

The application will start a server listening for webhook events from WhatsApp. Ensure that your webhook URL is correctly configured in the WhatsApp Business API settings.

## Extending the Bot

To create a custom bot, you can extend the BaseMessageHandler or modify the DefaultMessageHandler class and implement your own logic.

## Logging

Logs are written to whakit/logs/app.log and output to the console. You can configure logging settings in settings.py.

## License

This project is licensed under the MIT License.