# Import Packages
import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.ollama import OllamaChatPromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory

# Define main function
async def main():
   
    # Create Chat Completion Service. 
    chat_completion = OllamaChatCompletion(
       ai_model_id="llama3.2:latest",      # The Model we have
       host="http://localhost:11434/",     # The URL in which the Model is accessible
       service_id="my-service-id"          # The 'id' of the service
    )
    
    # Initialize the kernel
    kernel = Kernel()

    # Add/Register the Chat_Completion Service to/with the Kernel
    kernel.add_service(chat_completion)

    # Retrieve the chat completion service by id
    chat_completion_service = kernel.get_service(service_id="my-service-id")

    # Specific configuration options available when interacting with Ollama-hosted large language models for chat completion.
    # A bridge to customize the interaction between Semantic Kernel and your locally running Ollama models
    execution_settings = OllamaChatPromptExecutionSettings()

    # Create Chat_History Object. This will store the messages in the chat
    # It is used to store messages from different authors, such as users, assistants, tools, or the system. 
    # As the primary mechanism for sending and receiving messages, the chat history object is essential for maintaining context and continuity in a conversation.
    chat_history = ChatHistory()

    # Give it a message
    chat_history.add_user_message("Hello, Can you explain in under 50 words, what is GitBub?")

    # Get response of the message 
    response = await chat_completion_service.get_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings,
    )
    
    # Print the message
    print(response)

    
# Run the main function
if __name__ == "__main__":

    asyncio.run(main())

