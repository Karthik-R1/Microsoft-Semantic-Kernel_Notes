# Import Packages
import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.ollama import OllamaChatPromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents import ChatMessageContent, TextContent, ImageContent
from semantic_kernel.contents.utils.author_role import AuthorRole


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


    # Chat History Object:

    # => Store messages from different authors, such as users, assistants, tools, or the system. 
    # => These roles help differentiate who is sending a message and are stored within a ChatMessageContent object along with the message text and other metadata\
    # => Role Info:
        #   User: Represents the human user interacting with the AI. 
        #   Assistant: Represents the AI model's responses and contributions to the conversation. 
        #   System: Can be used to provide system-level instructions or information that influences the AI's behavior. 
        #   Tool: Represents the output or messages from integrated tools or other agents that the AI uses to perform tasks. 
    # => The ChatHistory object is essentially a collection of ChatMessageContent objects
    
    # ChatMessageContent:

    # => Each message in the ChatHistory object is stored in a ChatMessageContent object. 
    # => This object contains a role property that specifies the author of that message.
    # => When we add messages to the chat history, we define the role for each message, creating a clear and organized record of the conversation. 

    # Give a message
   # Add system message
    chat_history.add_message(
        ChatMessageContent(
            role=AuthorRole.SYSTEM,
            content="You are a helpful assistant"
        )
    )

    # Add assistant message
    chat_history.add_message(
        ChatMessageContent(
            role=AuthorRole.ASSISTANT,
            name="Restaurant Assistant",
            content="We have pizza, pasta, and salad available to order. What would you like to order?"
        )
    )

# Add additional message from a different user
    chat_history.add_message(
        ChatMessageContent(
            role=AuthorRole.USER,
            name="Ema Vargova",
            content="I'd like to have the first option, please."
        )
    )

    print("\nMessage: ", chat_history[0].content, "\nRole: ", chat_history[0].role)
    print("\nMessage: ", chat_history[1].content, "\nRole: ", chat_history[1].role)
    print("\nMessage: ", chat_history[2].content, "\nRole: ", chat_history[2].role)


    
# Run the main function
if __name__ == "__main__":

    asyncio.run(main())
