import functools
import json
import os
from typing import Dict, Tuple
from not_chipotle_service.order.models import Menu, MenuItem
from pydantic import TypeAdapter


@functools.cache
def load_menu() -> Tuple[Menu, Dict[str, MenuItem]]:
    """Load the menu from the JSON file"""
    menu_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "..",
        "config",
        "menu.json",
    )
    with open(menu_file_path, "r") as f:
        menu_data = json.load(f)
    menu_adapter = TypeAdapter(Menu)
    menu = menu_adapter.validate_python(menu_data)

    # Create a dictionary of menu items for easy access
    menu_items_dict = {}
    for item in menu.entrees:
        menu_items_dict[f"{item.type}|{item.id}"] = item
    for item in menu.proteins:
        menu_items_dict[f"{item.type}|{item.id}"] = item
    for item in menu.toppings:
        menu_items_dict[f"{item.type}|{item.id}"] = item
    for item in menu.sides:
        menu_items_dict[f"{item.type}|{item.id}"] = item
    for item in menu.drinks:
        menu_items_dict[f"{item.type}|{item.id}"] = item

    return menu, menu_items_dict