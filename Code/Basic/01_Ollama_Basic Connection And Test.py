
# Import necessary packages
import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.ollama  import OllamaChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.ollama.ollama_prompt_execution_settings import(OllamaChatPromptExecutionSettings)


async def main():

    # Initialize the kernel
    kernel = Kernel()

    # Add Ollama chat completion
    chat_completion = OllamaChatCompletion(
       ai_model_id="llama3.2:latest",
       host="http://localhost:11434/",
    )
    kernel.add_service(chat_completion)


    # Enable planning
    execution_settings = OllamaChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create a history of the conversation
    history = ChatHistory()

    # Initiate a back-and-forth chat
    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")

        # Terminate the loop when the user types "exit"
        if userInput == "exit":
            break

        # Add user input to the history
        history.add_user_message(userInput)

        # Get the response from the AI
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )

        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the agent to the chat history
        history.add_message(result)


# Run the main function
if __name__ == "__main__":

    asyncio.run(main())
