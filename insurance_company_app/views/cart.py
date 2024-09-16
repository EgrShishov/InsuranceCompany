import uuid
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from ..models.insurance_contract import InsuranceContract, InsuranceAgent, InsuranceObject


@login_required(login_url='login')
def cart_view(request):
    cart = request.session.get('cart', {})
    list_cart = []
    if cart:
        for cart_item in cart.values():
            agent_id = cart_item['agent']
            object_id = cart_item['object']
            cart_id = cart_item.get('id')
            print(cart_id)

            agent = InsuranceAgent.objects.get(id=agent_id)
            object = InsuranceObject.objects.get(id=object_id)
            list_cart.append({'id': cart_id, 'agent': f"{agent.surname} {agent.name} {agent.second_name}", 'object': object.name,
                              'sum': cart_item['sum'], 'quantity': cart_item['quantity']})

    total_price = sum(item['sum'] * item['quantity'] for item in list_cart)

    request.session['cart'] = cart
    request.session.modified = True

    return render(request, 'insurance/cart.html', {'cart': list_cart, 'total_price': total_price})

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    del cart[id]
    request.session.modified = True
    total_price = sum(item['sum'] * item['quantity'] for item in cart.values())

    return render(request, 'insurance/cart.html', {'cart': cart, 'total_price': total_price})


@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})
    if cart:
        total_price = sum(item['sum'] * item['quantity'] for item in cart.values())
    return render(request, 'insurance/checkout.html', {'total': total_price})
