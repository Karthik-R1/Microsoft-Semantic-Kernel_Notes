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
    chat_history.add_user_message("Hello, Can you explain in under 100 words, what is GitBub?")

    # Get response of the message 
    response = await chat_completion_service.get_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings,
    )
    print ("\n\nQuestion: Explain GitHub in 100 words.\n" , response)
    
    chat_history.add_user_message("Can you summarize previous response in under 20 words?")

    response = await chat_completion_service.get_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings,
    )
    print ("\n\nFolow-up Query: Rephrase previous reply in 20 words.\n", response)

    print ('\n\nPrinting Chat Messages:\n')
    # Access the chat messages from Chat History object and print the details:
    for message in chat_history.messages:
        print(f"Role: {message.role}, Content: {message.content}") 


    
# Run the main function
if __name__ == "__main__":

    asyncio.run(main())

