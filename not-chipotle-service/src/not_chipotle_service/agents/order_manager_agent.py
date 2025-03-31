from dataclasses import dataclass

from dotenv import load_dotenv
import not_chipotle_service.order.cart_operations as cart_ops
from not_chipotle_service.order.models import Cart, Menu
from pydantic_ai import Agent, RunContext


# Load environment variables from .env file
load_dotenv()

@dataclass
class OrderManagerAgentDeps:
    cart: Cart
    menu: Menu

order_manager_agent = Agent(
    model="google-gla:gemini-2.0-flash",
    deps_type=OrderManagerAgentDeps,
    system_prompt="""
    You are a helpful assistant for managing the construction of a Chipotle order.
    Your task is to assist the user in building their order by interacting with the menu and the shopping cart.
    You will help the user navigate through the menu, select items, and customize their order.
    You can add items to the cart, modify them, and finalize the order.
    Make sure to familiarize yourself with the menu items and their options by using the view_menu tool at the start of the conversation.

    Here are some guidelines to follow:
    - Greet the user and ask what they would like to order.
    - Assist the user in selecting items from the menu, including entrees, sides, and drinks.
    - Guide the user through the customization process for entrees (1. selecting protein, 2. rice, 3. beans, 4. other toppings).
    - Provide options for sides and drinks once the user has selected their entree(s).
    - Keep track of the items in the cart and provide updates on the current order.
    - If the user wants to remove an item or make changes to their order, assist them with that as well.
    - Ensure that the user is aware of their current cart contents and the total price as they build their order.
    - If the user asks for help or clarification, provide it in a friendly and informative manner.
    - Remember to use the tools available to you to interact with the cart and menu.
    - Always provide the user with the available options at each step of the ordering process.
    - If the user seems unsure, offer suggestions or ask clarifying questions to help them make a decision.
    - Be patient and understanding, as not everyone may be familiar with the menu or the ordering process.
    - If the user expresses any dietary restrictions or preferences, try to accommodate them by suggesting suitable menu items or modifications.
    - If the user goes off-topic or asks unrelated questions, gently steer the conversation back to their order.
    - Do not speak to the user about tools or functionality that you have access to. Instead, focus on assisting the user with their order.
    - Always check if there are any tools that should be called. Remember that an entree needs to be added to the cart before customizing it with toppings or proteins.
    """
)

@order_manager_agent.tool
def view_menu(ctx: RunContext[OrderManagerAgentDeps]) -> Menu:
    """View the menu items available for ordering."""
    
    menu = ctx.deps.menu
    
    return menu

@order_manager_agent.tool
def view_cart(ctx: RunContext[OrderManagerAgentDeps]) -> Cart:
    """View the current items in the cart."""
    
    cart = ctx.deps.cart
    
    return cart

@order_manager_agent.tool
def add_item_to_cart(ctx: RunContext[OrderManagerAgentDeps], item_type: str, menu_item_id: str) -> str:
    """Add an item to the cart."""

    index = cart_ops.add_item_to_cart(ctx.deps.cart, ctx.deps.menu, item_type, menu_item_id)
    
    print(f"[ DEBUG ] Added {item_type} with ID {menu_item_id} to the cart at index {index}.")

    # Return a confirmation message
    return f"Added {item_type} with ID {menu_item_id} to the cart at index {index}."

@order_manager_agent.tool
def remove_item_from_cart(ctx: RunContext[OrderManagerAgentDeps], item_index: int) -> str:
    """Remove an item from the cart based on its index."""
    
    cart_ops.remove_item_from_cart(ctx.deps.cart, item_index)
    
    print(f"[ DEBUG ] Removed item at index {item_index} from the cart.")

    # Return a confirmation message
    return f"Removed item at index {item_index} from the cart."

@order_manager_agent.tool
def add_topping_to_entree(ctx: RunContext[OrderManagerAgentDeps], item_index: int, topping_id: str) -> str:
    """Add a topping to an entree in the cart based on its index."""
    
    try:
        cart_ops.add_topping_to_entree(ctx.deps.cart, ctx.deps.menu, item_index, topping_id)
        print(f"[ DEBUG ] Added topping with ID {topping_id} to entree at index {item_index}.")
        
        # Return a confirmation message
        return f"Added topping with ID {topping_id} to entree at index {item_index}."
    except ValueError as e:
        print(f"[ DEBUG ] Error adding topping: {str(e)}")
        return str(e)
    
@order_manager_agent.tool
def remove_topping_from_entree(ctx: RunContext[OrderManagerAgentDeps], item_index: int, topping_id: str) -> str:
    """Remove a topping from an entree in the cart based on its index."""
    
    try:
        cart_ops.remove_topping_from_entree(ctx.deps.cart, item_index, topping_id)
        print(f"[ DEBUG ] Removed topping with ID {topping_id} from entree at index {item_index}.")
        
        # Return a confirmation message
        return f"Removed topping with ID {topping_id} from entree at index {item_index}."
    except ValueError as e:
        print(f"[ DEBUG ] Error removing topping: {str(e)}")
        return str(e)
    
@order_manager_agent.tool
def set_entree_protein(ctx: RunContext[OrderManagerAgentDeps], item_index: int, new_protein_id: str) -> str:
    """Set the protein for an entree in the cart based on its index."""
    
    try:
        index = cart_ops.set_entree_protein(ctx.deps.cart, ctx.deps.menu, item_index, new_protein_id)
        print(f"[ DEBUG ] Set protein with ID {new_protein_id} for entree at index {item_index}.")
        
        # Return a confirmation message
        return f"Set protein with ID {new_protein_id} for entree at index {index}."
    except ValueError as e:
        print(f"[ DEBUG ] Error setting protein: {str(e)}")
        return str(e)
    
# @order_manager_agent.tool
# def set_entree_special_configurations(ctx: RunContext[OrderManagerAgentDeps], item_index: int, special_configurations: dict) -> str:
#     """Set special configurations for an entree in the cart based on its index."""
    
#     try:
#         index = cart_ops.set_entree_special_configurations(ctx.deps.cart, ctx.deps.menu, item_index, special_configurations)
#         print(f"[ DEBUG ] Set special configurations for entree at index {item_index}: {special_configurations}.")
        
#         # Return a confirmation message
#         return f"Set special configurations for entree at index {index}: {special_configurations}."
#     except ValueError as e:
#         print(f"[ DEBUG ] Error setting special configurations: {str(e)}")
#         return str(e)