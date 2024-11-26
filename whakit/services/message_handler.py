# whakit/services/message_handler.py

import logging
from abc import ABC, abstractmethod
from datetime import datetime

from whakit.config.settings import settings
from whakit.services.ai import AIService

# from whakit.services.storage import StorageService
from whakit.services.whatsapp import WhatsAppService
from whakit.state.manager import StateManager


class BaseMessageHandler(ABC):
    @abstractmethod
    async def handle_incoming_message(self, message: dict, sender_info: dict):
        """Process an incoming message."""
        pass

    @abstractmethod
    def is_greeting(self, message: str) -> bool:
        """Determine if a message is a greeting."""
        pass

    @abstractmethod
    async def send_welcome_message(self, to: str, sender_info: dict):
        """Send a welcome message to the user."""
        pass

    @abstractmethod
    async def send_main_menu(self, to: str):
        """Send the main menu to the user."""
        pass

    async def pre_process_message(self, message: dict):
        """Hook called before processing a message."""
        pass

    async def post_process_message(self, response: dict):
        """Hook called after processing a message."""
        pass


logger = logging.getLogger(__name__)


class DefaultMessageHandler(BaseMessageHandler):
    def __init__(self):
        self.whatsapp_service = WhatsAppService()
        self.ai_service = AIService()
        # self.storage_service = StorageService()
        self.state_manager = StateManager()
        self.appointment_state = {}
        self.assistant_state = {}

    async def handle_incoming_message(self, message: dict, sender_info: dict):
        await self.pre_process_message(message)
        from_number = message.get("from")
        message_type = message.get("type")

        if message_type == "text":
            incoming_message = message["text"]["body"].lower().strip()
            print(f"Received message: {incoming_message}")

            if self.is_greeting(incoming_message):
                await self.send_welcome_message(from_number, sender_info)
                await self.send_main_menu(from_number)
            elif from_number in self.appointment_state:
                await self.handle_appointment_flow(from_number, incoming_message)
            elif from_number in self.assistant_state:
                await self.handle_assistant_flow(from_number, incoming_message)
            else:
                await self.handle_menu_option(from_number, incoming_message)
            await self.whatsapp_service.mark_as_read(message["id"])
        elif message_type == "interactive":
            option = message["interactive"]["button_reply"]["id"]
            await self.handle_menu_option(from_number, option)
            await self.whatsapp_service.mark_as_read(message["id"])
        else:
            logger.info(f"Unhandled message type: {message_type}")
        await self.post_process_message({"status": "success"})

    def is_greeting(self, message: str) -> bool:
        greetings = settings.GREETINGS
        return message in greetings

    async def send_welcome_message(self, to: str, sender_info: dict):
        name = sender_info.get("profile", {}).get("name", to)
        welcome_message = settings.WELCOME_MESSAGE.format(name=name)
        await self.whatsapp_service.send_message(to, welcome_message)

    async def send_main_menu(self, to: str):
        menu_message = settings.MENU_MESSAGE
        buttons = settings.MENU_BUTTONS
        await self.whatsapp_service.send_interactive_message(to, menu_message, buttons)

    async def handle_menu_option(self, to: str, option: str):
        if option == "option_1":
            self.appointment_state[to] = {"step": "name"}
            response = "Please enter your name:"
            await self.whatsapp_service.send_message(to, response)
        elif option == "option_2":
            self.assistant_state[to] = {"step": "question"}
            response = "Please ask your question:"
            await self.whatsapp_service.send_message(to, response)
        elif option == "option_3":
            response = "Here is our location:"
            await self.whatsapp_service.send_message(to, response)
            await self.send_location(to)
        else:
            response = "Sorry, I didn't understand your selection. Please choose an option from the menu."
            await self.whatsapp_service.send_message(to, response)

    async def handle_appointment_flow(self, to: str, message: str):
        state = self.appointment_state[to]
        if state["step"] == "name":
            state["name"] = message
            state["step"] = "pet_name"
            response = "Thank you. What is your pet's name?"
        elif state["step"] == "pet_name":
            state["pet_name"] = message
            state["step"] = "pet_type"
            response = "What type of pet is it? (e.g., dog, cat, etc.)"
        elif state["step"] == "pet_type":
            state["pet_type"] = message
            state["step"] = "reason"
            response = "What is the reason for the appointment?"
        elif state["step"] == "reason":
            state["reason"] = message
            response = await self.complete_appointment(to)
        else:
            response = "An error occurred. Let's start over."
            del self.appointment_state[to]
        await self.whatsapp_service.send_message(to, response)

    async def complete_appointment(self, to: str) -> str:
        appointment = self.appointment_state[to]
        del self.appointment_state[to]

        user_data = [
            to,
            appointment["name"],
            appointment["pet_name"],
            appointment["pet_type"],
            appointment["reason"],
            datetime.utcnow().isoformat(),
        ]
        # Append data to Google Sheets
        # spreadsheet_id = (
        #     "your_spreadsheet_id_here"  # Replace with your actual spreadsheet ID
        # )
        # await self.storage_service.append_to_sheet(spreadsheet_id, user_data)

        return f"""Thank you for scheduling an appointment.
        Here is a summary:

        Name: {appointment['name']}
        Pet Name: {appointment['pet_name']}
        Pet Type: {appointment['pet_type']}
        Reason: {appointment['reason']}

        We will contact you soon to confirm the date and time."""

    async def handle_assistant_flow(self, to: str, message: str):
        state = self.assistant_state.get(to, {})
        step = state.get('step', 'question')

        if step == 'question':
            # Retrieve the existing chat history
            chat_history = self.state_manager.get_chat_history(to)
            # Append the user's message to the chat history
            self.state_manager.append_chat_history(to, f"Human: {message}")

            # Combine the chat history into a single string
            chat_history_str = "\n".join(chat_history)

            # Generate response using AI service with chat history
            response = await self.ai_service.generate_response(message, chat_history=chat_history_str)

            # Send the AI's response
            await self.whatsapp_service.send_message(to, response)

            # Append the AI's response to the chat history
            self.state_manager.append_chat_history(to, f"AI: {response}")

            # Ask if the question was answered
            confirmation_message = "Did that answer your question? (Yes/No)"
            await self.whatsapp_service.send_message(to, confirmation_message)

            # Update the assistant state
            self.assistant_state[to]['step'] = 'confirmation'

        elif step == 'confirmation':
            # Check the user's response
            if message.lower() in ['yes', 'y']:
                # End the assistant flow
                await self.whatsapp_service.send_message(to, "Glad I could help!")
                del self.assistant_state[to]
                # Clear chat history if desired
                self.state_manager.clear_chat_history(to)
            elif message.lower() in ['no', 'n']:
                # Continue to wait for user input
                await self.whatsapp_service.send_message(to, "I'm sorry to hear that. Please provide more details or ask another question.")
                # Reset the step to 'question' to process the next input
                self.assistant_state[to]['step'] = 'question'
            else:
                # If the input is not clear, ask again
                await self.whatsapp_service.send_message(to, "Please reply with 'Yes' or 'No'.")
        else:
            # Handle unexpected state
            await self.whatsapp_service.send_message(to, "An error occurred. Let's start over.")
            del self.assistant_state[to]
            self.state_manager.clear_chat_history(to)

    async def send_location(self, to: str):
        latitude = 40.712776
        longitude = -74.005974
        name = "Our Location"
        address = "123 Main St, New York, NY"
        await self.whatsapp_service.send_location_message(
            to, latitude, longitude, name, address
        )
