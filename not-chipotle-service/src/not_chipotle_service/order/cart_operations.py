from typing import Optional, Dict
from not_chipotle_service.order.models import (
    Cart,
    Menu,
    CartEntree,
    CartSide,
    CartDrink,
)


def _get_entree_from_cart(
    cart: Cart, item_index: int
) -> Optional[CartEntree]:
    """Helper function to get a specific CartEntree from the cart."""
    # Make sure a valid item_index is provided
    if item_index < 0 or item_index >= len(cart.items):
        return None

    # Get the item at the specified index
    cart_item = cart.items[item_index]

    # Check if the item is a CartEntree
    if isinstance(cart_item, CartEntree):
        return cart_item

    # If it's not an entree, return None
    return None


def add_item_to_cart(
    cart: Cart,
    menu: Menu,
    item_type: str,
    menu_item_id: str,
) -> Cart:
    """Adds an item to the shopping cart based on the item type and menu item ID."""
    if item_type == "entree":
        menu_item = next((item for item in menu.entrees if item.id == menu_item_id), None)
        if menu_item:
            cart.items.append(CartEntree(menu_item_id=menu_item_id, quantity=1))
        else:
            raise ValueError(f"Entree with ID '{menu_item_id}' not found in the menu.")
    elif item_type == "side":
        menu_item = next((item for item in menu.sides if item.id == menu_item_id), None)
        if menu_item:
            cart.items.append(CartSide(menu_item_id=menu_item_id, quantity=1))
        else:
            raise ValueError(f"Side with ID '{menu_item_id}' not found in the menu.")
    elif item_type == "drink":
        menu_item = next((item for item in menu.drinks if item.id == menu_item_id), None)
        if menu_item:
            cart.items.append(CartDrink(menu_item_id=menu_item_id, quantity=1))
        else:
            raise ValueError(f"Drink with ID '{menu_item_id}' not found in the menu.")
    else:
        raise ValueError(
            f"Invalid item_type: '{item_type}'. Must be 'entree', 'side', or 'drink'."
        )

    return cart


def remove_item_from_cart(cart: Cart, item_index: int) -> Cart:
    """Removes an item from the shopping cart by index."""
    if item_index < 0 or item_index >= len(cart.items):
        raise ValueError(f"Invalid index: {item_index}. Cannot remove item from cart.")
    
    removed_item = cart.items.pop(item_index)
    return cart


def add_topping_to_entree(cart: Cart, menu: Menu, item_index: int, topping_id: str) -> Cart:
    """Adds a topping to a specific entree in the cart."""
    # Make sure a valid item_index is provided
    if item_index < 0 or item_index >= len(cart.items):
        raise ValueError(f"Invalid index: {item_index}. Cannot add topping to entree.")

    # Get the entree from the cart and verify it's an entree
    entree = _get_entree_from_cart(cart, item_index)
    if not entree:
        raise ValueError(f"Menu item index '{item_index}' is not an entree.")

    # Check if the topping exists in the menu
    topping_exists = any(topping.id == topping_id for topping in menu.toppings)
    if not topping_exists:
        raise ValueError(f"Topping with ID '{topping_id}' not found in the menu.")

    # Add the topping if it is not already present
    if topping_id not in entree.toppings:
        entree.toppings.append(topping_id)

    return cart


def remove_topping_from_entree(cart: Cart, item_index: int, topping_id: str) -> Cart:
    """Removes a topping from a specific entree in the cart."""
    entree = _get_entree_from_cart(cart, item_index)
    if not entree:
        raise ValueError(f"Menu item index '{item_index}' is not an entree.")

    if topping_id in entree.toppings:
        entree.toppings.remove(topping_id)
    return cart


def set_entree_protein(
    cart: Cart,
    menu: Menu,
    item_index: int,
    new_protein_id: str,
) -> Cart:
    """Sets the protein of a specific entree in the cart."""
    entree = _get_entree_from_cart(cart, item_index)
    if not entree:
        raise ValueError(f"Menu item index '{item_index}' is not an entree.")

    protein_exists = any(protein.id == new_protein_id for protein in menu.proteins)
    if not protein_exists:
        raise ValueError(f"Protein with ID '{new_protein_id}' not found in the menu.")
    entree.protein_id = new_protein_id

    return cart


def set_entree_special_configurations(
    cart: Cart,
    menu: Menu,
    item_index: int,
    special_configurations: Dict,
) -> Cart:
    """Configures the special configurations for a specific entree in the cart."""
    entree = _get_entree_from_cart(cart, item_index)
    if not entree:
        raise ValueError(f"Menu item index '{item_index}' is not an entree.")

    # Get the menu item to check its allowed special configurations
    menu_item = next((item for item in menu.entrees if item.id == entree.menu_item_id), None)
    if not menu_item or not menu_item.special_configurations:
        raise ValueError(f"Entree '{entree.menu_item_id}' does not support special configurations")
    
    # Validate each provided configuration
    for config_key, config_value in special_configurations.items():
        # Check if this configuration type is allowed for this entree
        if config_key not in menu_item.special_configurations:
            raise ValueError(f"Configuration '{config_key}' is not supported for {entree.menu_item_id}")
        
        # Check if the value is in the allowed values for this configuration
        allowed_values = menu_item.special_configurations.get(config_key)
        if allowed_values and config_value not in allowed_values:
            raise ValueError(
                f"Invalid value '{config_value}' for configuration '{config_key}'. "
                f"Allowed values: {', '.join(allowed_values)}"
            )
    
    entree.special_configurations = special_configurations
    return cart


def print_cart(cart: Cart):
    """Prints the contents of the cart in a more readable format with emojis."""
    if not cart.items:
        print("🛒 Your cart is empty.")
        return

    print(f"🛒 Cart ID: {cart.cart_id}")
    for item in cart.items:
        if isinstance(item, CartEntree):
            print(f"  🌯 Entree: {item.menu_item_id} (x{item.quantity})")
            if item.protein_id:
                print(f"    🐥 Protein: {item.protein_id}")
            if item.toppings:
                print(f"    🫘 Toppings: {', '.join(item.toppings)}")
            if item.special_configurations:
                print(f"    ⚙️ Configurations: {item.special_configurations}")
        elif isinstance(item, CartSide):
            print(f"  🥑 Side: {item.menu_item_id} (x{item.quantity})")
        elif isinstance(item, CartDrink):
            print(f"  💧 Drink: {item.menu_item_id} (x{item.quantity})")
        else:
            print(f"  ❓ Unknown Item: {item.menu_item_id} (x{item.quantity})")
