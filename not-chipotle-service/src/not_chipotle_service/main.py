import asyncio
import json
import os
from pydantic import TypeAdapter
from not_chipotle_service.order.models import Menu, Cart
import not_chipotle_service.order.cart_operations as cart_ops
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, UserPromptPart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def main():
    """Enables users to chat with Gemini 2.0 Flash in the terminal, keeping full chat history."""

    agent = Agent(
        "google-gla:gemini-2.0-flash",
        system_prompt="You are a helpful and friendly chatbot.  Reply in a conversational tone.",
    )

    chat_history: list[ModelMessage] = []

    print("Welcome to the Gemini 2.0 Flash Chatbot!")
    print("Type 'exit' to end the chat.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        result = await agent.run(
            user_input, message_history=chat_history
        )
        chat_history.extend(result.new_messages())  # save new exchanged message

        print(f"Gemini: {result.data}\n")

# def main():
#     """Entry point for the NotChipotle service."""
#     print("Starting my awesome service using main.py!")
    
#     try:
#         menu_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config", "menu.json")
#         print(f"Loading menu from: {menu_file_path}")
#         with open(menu_file_path, "r") as f:
#             menu_data = json.load(f)
#         menu_adapter = TypeAdapter(Menu)
#         menu = menu_adapter.validate_python(menu_data)
#         cart = Cart(cart_id="user_cart_123")

#         # Empty cart
#         print("\n\nInitial empty cart:")
#         cart_ops.print_cart(cart)

#         # Add items
#         cart = cart_ops.add_item_to_cart(cart, menu, "entree", "burrito", quantity=1, protein_id="chicken", toppings=["white_rice", "black_beans"])
#         cart = cart_ops.add_item_to_cart(cart, menu, "side", "chips", quantity=2)
#         cart = cart_ops.add_item_to_cart(cart, menu, "drink", "fountain_small")
#         print("\n\nCart after adding initial items:")
#         cart_ops.print_cart(cart)

#         # Add a second burrito
#         cart = cart_ops.add_item_to_cart(cart, menu, "entree", "burrito", quantity=1, protein_id="barbacoa", toppings=["white_rice", "black_beans", "corn_salsa"])
#         print("\n\nCart after adding a second burrito:")
#         cart_ops.print_cart(cart)

#         # Add a topping to the first burrito
#         cart = cart_ops.add_topping_to_entree(cart, menu, "burrito", "guacamole", item_index=0)
#         print("\n\nCart after adding guacamole to the first burrito:")
#         cart_ops.print_cart(cart)

#         # Remove items
#         cart = cart_ops.remove_item_from_cart(cart, "chips", quantity=2)
#         print("\n\nCart after removing two chips:")
#         cart_ops.print_cart(cart)

#         # Add tacos
#         cart = cart_ops.add_item_to_cart(cart, menu, "entree", "tacos", quantity=1)
#         print("\n\nCart after adding tacos:")
#         cart_ops.print_cart(cart)

#         # Configure special configurations for tacos (e.g., number of tortillas)
#         cart = cart_ops.configure_entree_special_configurations(cart, menu, "tacos", special_configurations={"taco_type": "flour"})
#         print("\n\nCart after configuring tacos:")
#         cart_ops.print_cart(cart)

#     except FileNotFoundError:
#         print("Error: menu.json not found. Please create this file in the same directory.")
#     except json.JSONDecodeError:
#         print("Error: Could not decode menu.json. Please ensure it is valid JSON.")
#     except ValueError as e:
#         print(f"Error: {e}")

def run():
    """Entry point for the NotChipotle service."""
    print("Starting my awesome service using main.py!")
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
