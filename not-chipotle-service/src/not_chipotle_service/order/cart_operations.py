from typing import Optional, List, Dict
from src.not_chipotle_service.order.models import Cart, Menu, CartItem, CartEntree, CartSide, CartDrink

def add_item_to_cart(cart: Cart, menu: Menu, item_type: str, menu_item_id: str, quantity: int = 1, protein_id: Optional[str] = None, toppings: Optional[List[str]] = None, special_configurations: Optional[Dict] = None) -> Cart:
    """Adds an item to the shopping cart."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    menu_item = None
    if item_type == "entree":
        menu_item = next((item for item in menu.entrees if item.id == menu_item_id), None)
        if menu_item:
            if protein_id:
                protein_exists = any(protein.id == protein_id for protein in menu.proteins)
                if not protein_exists:
                    raise ValueError(f"Protein with ID '{protein_id}' not found in the menu.")
            if toppings:
                for topping_id in toppings:
                    topping_exists = any(topping.id == topping_id for topping in menu.toppings)
                    if not topping_exists:
                        raise ValueError(f"Topping with ID '{topping_id}' not found in the menu.")
            cart.items.append(CartEntree(menu_item_id=menu_item_id, quantity=quantity, protein_id=protein_id, toppings=toppings or [], special_configurations=special_configurations))
        else:
            raise ValueError(f"Entree with ID '{menu_item_id}' not found in the menu.")
    elif item_type == "side":
        menu_item = next((item for item in menu.sides if item.id == menu_item_id), None)
        if menu_item:
            cart.items.append(CartSide(menu_item_id=menu_item_id, quantity=quantity))
        else:
            raise ValueError(f"Side with ID '{menu_item_id}' not found in the menu.")
    elif item_type == "drink":
        menu_item = next((item for item in menu.drinks if item.id == menu_item_id), None)
        if menu_item:
            cart.items.append(CartDrink(menu_item_id=menu_item_id, quantity=quantity))
        else:
            raise ValueError(f"Drink with ID '{menu_item_id}' not found in the menu.")
    else:
        raise ValueError(f"Invalid item_type: '{item_type}'. Must be 'entree', 'side', or 'drink'.")

    return cart

def remove_item_from_cart(cart: Cart, menu_item_id: str, quantity: int = 1) -> Cart:
    """Removes a specified quantity of an item from the shopping cart."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    items_to_remove = quantity
    updated_items = []
    for item in cart.items:
        if item.menu_item_id == menu_item_id:
            if items_to_remove > 0:
                if item.quantity > items_to_remove:
                    updated_items.append(item.model_copy(update={"quantity": item.quantity - items_to_remove}))
                    items_to_remove = 0
                else:
                    items_to_remove -= item.quantity
            else:
                updated_items.append(item)
        else:
            updated_items.append(item)

    cart.items = updated_items
    return cart

def update_item_quantity_in_cart(cart: Cart, menu_item_id: str, new_quantity: int) -> Cart:
    """Updates the quantity of a specific item in the shopping cart."""
    if new_quantity < 1:
        raise ValueError("New quantity must be at least 1.")

    updated = False
    for item in cart.items:
        if item.menu_item_id == menu_item_id:
            item.quantity = new_quantity
            updated = True
            break  # Assuming we update the first matching item
    if not updated:
        raise ValueError(f"Item with ID '{menu_item_id}' not found in the cart.")
    return cart

def add_topping_to_entree(cart: Cart, menu: Menu, menu_item_id: str, topping_id: str, item_index: Optional[int] = None) -> Cart:
    """Adds a topping to a specific entree in the cart."""
    entree = _get_specific_cart_entree(cart, menu_item_id, item_index)
    if not entree:
        raise ValueError(f"Entree with ID '{menu_item_id}' not found in the cart.")

    topping_exists_in_menu = any(t.id == topping_id for t in menu.toppings)
    if not topping_exists_in_menu:
        raise ValueError(f"Topping with ID '{topping_id}' not found in the menu.")

    if topping_id not in entree.toppings:
        entree.toppings.append(topping_id)
    return cart

def remove_topping_from_entree(cart: Cart, menu: Menu, menu_item_id: str, topping_id: str, item_index: Optional[int] = None) -> Cart:
    """Removes a topping from a specific entree in the cart."""
    entree = _get_specific_cart_entree(cart, menu_item_id, item_index)
    if not entree:
        raise ValueError(f"Entree with ID '{menu_item_id}' not found in the cart.")

    if topping_id in entree.toppings:
        entree.toppings.remove(topping_id)
    return cart

def _get_specific_cart_entree(cart: Cart, menu_item_id: str, item_index: Optional[int] = None) -> Optional[CartEntree]:
    """Helper function to get a specific CartEntree from the cart."""
    if item_index is not None:
        if 0 <= item_index < len(cart.items):
            item = cart.items[item_index]
            if isinstance(item, CartEntree) and item.menu_item_id == menu_item_id:
                return item
            else:
                raise ValueError(f"No entree with ID '{menu_item_id}' found at index {item_index} in the cart.")
        else:
            raise ValueError(f"Invalid item index: {item_index} for the cart.")
    else:
        for item in cart.items:
            if isinstance(item, CartEntree) and item.menu_item_id == menu_item_id:
                return item
        return None

def change_entree_protein(cart: Cart, menu: Menu, menu_item_id: str, item_index: Optional[int] = None, protein_id: Optional[str] = None) -> Cart:
    """Changes the protein of a specific entree in the cart."""
    entree = _get_specific_cart_entree(cart, menu_item_id, item_index)
    if not entree:
        raise ValueError(f"Entree with ID '{menu_item_id}' not found in the cart.")

    if protein_id is not None:
        protein_exists = any(protein.id == protein_id for protein in menu.proteins)
        if not protein_exists:
            raise ValueError(f"Protein with ID '{protein_id}' not found in the menu.")
        entree.protein_id = protein_id

    return cart

def configure_entree_special_configurations(cart: Cart, menu: Menu, menu_item_id: str, special_configurations: Dict, item_index: Optional[int] = None) -> Cart:
    """Configures the special configurations for a specific entree in the cart."""
    entree = _get_specific_cart_entree(cart, menu_item_id, item_index)
    if not entree:
        raise ValueError(f"Entree with ID '{menu_item_id}' not found in the cart.")

    # You might want to add validation for the special configurations based on the menu
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