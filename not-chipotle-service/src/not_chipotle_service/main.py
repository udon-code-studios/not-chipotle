import asyncio
import logfire
from not_chipotle_service.agents.order_manager_agent import (
    OrderManagerAgentDeps,
    order_manager_agent,
)
from not_chipotle_service.order.models import Cart
import not_chipotle_service.order.cart_operations as cart_ops
import not_chipotle_service.order.utils as order_utils
from pydantic_ai.messages import ModelMessage
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

logfire.configure()


async def main():
    """Enables users to chat with Gemini 2.0 Flash in the terminal, keeping full chat history."""

    # Load the menu and initialize the cart
    menu, menu_items_dict = order_utils.load_menu()
    cart = Cart(cart_id="user_cart_123")

    print("Welcome to the Gemini 2.0 Flash Chatbot!")
    print("Type 'exit' to end the chat.\n")

    chat_history: list[ModelMessage] = []

    # Initialize the chat with a greeting message from the agent
    result = await order_manager_agent.run(
        user_prompt="Greet the user and ask what you could start them off with today. Your response to this will be shown to the user as the first message in the chat.",
        message_history=chat_history,
        deps=OrderManagerAgentDeps(cart=cart, menu=menu),
    )
    chat_history.extend(result.new_messages())
    print(f"\n\nGemini: {result.data}\n")

    while True:
        user_input = input("You: ")
        print()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        result = await order_manager_agent.run(
            user_prompt=user_input,
            message_history=chat_history,
            deps=OrderManagerAgentDeps(cart=cart, menu=menu),
        )
        chat_history.extend(result.new_messages())
        print(f"Gemini: {result.data}")

        # Print the current state of the cart after each interaction
        print("Current Cart:")
        cart_ops.print_cart(cart, menu_items_dict)
        print("\n")


def run():
    """Entry point for the NotChipotle service."""
    print("Invoking the NotChipotle service via run()...")

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    print("Invoking the NotChipotle service via __main__...")
    asyncio.run(main())
