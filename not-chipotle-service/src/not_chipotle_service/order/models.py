from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class CartItem(BaseModel):
    menu_item_id: str = Field(description="ID of the menu item (e.g., 'burrito', 'chicken', 'white_rice')")

class CartEntree(CartItem):
    menu_item_id: str = Field(description="ID of the entree (e.g., 'burrito', 'tacos')")
    protein_id: Optional[str] = Field(default=None, description="ID of the selected protein")
    toppings: List[str] = Field(default_factory=list, description="List of IDs of selected toppings")
    special_configurations: Optional[Dict] = Field(default=None, description="Special configurations for the entree (e.g., taco type)")

    @property
    def item_type(self) -> str:
        return "entree"

class CartSide(CartItem):
    menu_item_id: str = Field(description="ID of the side item (e.g., 'guacamole', 'chips')")

    @property
    def item_type(self) -> str:
        return "side"

class CartDrink(CartItem):
    menu_item_id: str = Field(description="ID of the drink item (e.g., 'fountain_small', 'bottled_water')")

    @property
    def item_type(self) -> str:
        return "drink"

class Cart(BaseModel):
    cart_id: str = Field(description="Unique identifier for the shopping cart")
    items: List[CartItem] = Field(default_factory=list, description="List of items in the cart")

class Order(BaseModel):
    order_id: str = Field(description="Unique identifier for the order")
    cart_id: str = Field(description="ID of the cart that was used to create this order")
    items: List[CartItem] = Field(description="List of items in the order (could be a copy of the cart items or more detailed)")
    total_price: float = Field(description="Total price of the order")
    customer_name: Optional[str] = Field(default=None, description="Name of the customer placing the order")

class MenuItem(BaseModel):
    id: str = Field(description="Unique identifier for the menu item")
    type: str = Field(description="Type of the menu item (e.g., 'entree', 'protein', 'topping', 'side', 'drink')")
    name: str = Field(description="Name of the menu item")
    price: Optional[float] = Field(default=None, description="Price of the menu item (for sides and drinks)")
    description: Optional[str] = Field(default=None, description="Description of the menu item")
    synonyms: Optional[List[str]] = Field(default_factory=list, description="List of synonyms for the menu item")
    special_configurations: Optional[Dict[str, List[str]]] = Field(default=None, description="Special configurations for the menu item (e.g., taco types)")

class Menu(BaseModel):
    entrees: List[MenuItem] = Field(default_factory=list, description="List of entree menu items (e.g., burrito, tacos)")
    proteins: List[MenuItem] = Field(default_factory=list, description="List of proteins which can be added to entrees (e.g., chicken, barbacoa)")
    toppings: List[MenuItem] = Field(default_factory=list, description="List of toppings which can be added to entrees (e.g., guacamole, cheese)")
    sides: List[MenuItem] = Field(default_factory=list, description="List of side menu items (e.g., chips, rice)")
    drinks: List[MenuItem] = Field(default_factory=list, description="List of drink menu items (e.g., fountain_small, bottled_water)")