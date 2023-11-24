from django.db.models import Sum

def generate_uid():
    import uuid
    uid = uuid.uuid4().hex[-8:]
    return uid

def add_order_item(request):
    from jresto.models import CustomUser, Product, Order, OrderItem
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

def check_cart_function(id):
    from jresto.models import CustomUser, Order
    try:
        customer_id = id
        customer = CustomUser.objects.get(id=customer_id)
        orders = Order.objects.filter(customer=customer, complete=False)
        total_cart_items = orders.aggregate(Sum('orderitem__quantity'))['orderitem__quantity__sum']
    except Exception as e:
        total_cart_items = {}
    return total_cart_items

def get_wallet(id):
    from jresto.models import Customer
    try:
        customer = Customer.objects.get(customer_id=id)
        cash = customer.cash
    except Customer.DoesNotExist:
        cash = 0

    return cash