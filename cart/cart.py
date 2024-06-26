from shop.models import ProductModel,ProductStatusType
from cart.models import CartModel,CartItemModel

class CartSession:
    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart", {"items": []})

    def update_product_quantity(self,product_id,quantity):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] = int(quantity)
                break
        else:
            return
        self.save()
        
    def remove_product(self,product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                self._cart["items"].remove(item)
                break
        else:
            return
        self.save()
        
    def add_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] += 1
                break
        else:
            new_item = {"product_id": product_id, "quantity": 1}
            self._cart["items"].append(new_item)
        self.save()
        
    def get_cart_dict(self):
        return self._cart
    
    def get_total_payment_amount(self):
        return sum(item["total_price"] for item in self._cart["items"])
    
    def get_total_quantity(self):
        return sum(item["quantity"] for item in self._cart["items"])
    
    def get_cart_items(self):
        for item in self._cart["items"]:
            product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            item.update({"product_obj": product_obj, "total_price": item["quantity"] * product_obj.get_price()})
        return self._cart["items"]
    
    def save(self):
        self.session.modified = True
        
    def clear(self):
        self._cart = self.session["cart"] = {"items": []}
        self.save()
    
    