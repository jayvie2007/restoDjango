def generate_uid():
    import uuid
    uid = uuid.uuid4().hex[-8:]
    return uid

def add_order_item(request):
    from .models import CustomUser, Product, Order, OrderItem
    customer_id = request.user.id
    customer = CustomUser.objects.get(id=customer_id)
    
    #Add orderitems into the customer users
    if request.method == "POST":
        product_id = request.POST['product_id']
        product_item = Product.objects.get(id=product_id)

        orders, created = Order.objects.get_or_create(customer = customer, complete = False)
        orderitems, created = OrderItem.objects.get_or_create(order = orders, product = product_item)
        
        if orderitems:
            orderitems.quantity = (orderitems.quantity + 1)
        orderitems.save()