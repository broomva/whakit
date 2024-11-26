# whakit/services/ai_service.py

import asyncio
import logging

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI

from whakit.config.settings import settings

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name="gpt-4o-mini",
            temperature=0  # Set temperature for deterministic output
        )

        # Initialize tools (you can add more tools as needed)
        self.tools = []  # List of tools the agent can use

        # Load the ReAct prompt that supports chat history
        self.prompt = hub.pull("hwchase17/react-chat")

        # Create the ReAct agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )

        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True  # Set to True for debugging
        )

    async def generate_response(self, user_message: str, chat_history: str = "") -> str:
        # Since the agent executor might not support async, use run_in_executor
        loop = asyncio.get_event_loop()
        try:
            response = await loop.run_in_executor(
                None,
                self.agent_executor.invoke,
                {"input": user_message, "chat_history": chat_history}
            )
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return "I'm sorry, I couldn't process your request at this time."