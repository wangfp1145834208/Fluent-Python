def fidelity_promo(order:'Order'):
    'fidelity promotion'
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

def bulk_item_promo(order:'Order'):
    'bulk item promotion'
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

def large_order_promo(order:'Order'):
    'large_order_promotion'
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0
