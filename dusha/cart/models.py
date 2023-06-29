from django.conf import settings

from coupon.models import Coupon
from item.models import Item

from decimal import Decimal


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}

        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def __len__(self):
        return sum(cart_item['quantity'] for cart_item in self.cart.values())


    def __iter__(self):
        Item_ids =   self.cart.keys()

        items = Item.objects.filter(id__in=Item_ids)

        for item in items:
            self.cart[str(item.id)]['item'] = item

        for cart_item in self.cart.values():
            cart_item['itme_price'] = Decimal(cart_item['item_price'])
            cart_item['total_price'] = Decimal( cart_item['item_price']) * cart_item['quantity']

            yield cart_item

    def add(self, item, quantity=1, is_update=False):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity':0, 'item_price':str(item.item_price)}

        if is_update:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del(self.cart[item_id])
            self.save()

    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session['coupon_id'] = None
        self.session.modified = True

    #전체 제품 가격
    def get_product_total(self):
        return sum(Decimal(cart_item['item_price']) * cart_item['quantity'] for cart_item in self.cart.values())


    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)  # 데이터 베이스에서 쿠폰 가져오기

    # 할인 금액
    def get_discount_total(self):
        if self.coupon:
            if self.get_product_total() >= self.coupon.discount:
                return self.coupon.discount
        return Decimal(0)

    # 할인 금액이 반영된 상품 금액
    def get_total_price(self):
        return self.get_product_total() - self.get_discount_total()

