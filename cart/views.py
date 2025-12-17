from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from shop.models import ProductVariant, Flavour, Product
from .models import CartItem

# Create your views here.


@login_required
def view_cart(req):
    cart_items = CartItem.objects.filter(user=req.user)
    cart_data = []
    total = sum(item.variant.price * item.quantity for item in cart_items)
    for item in cart_items:
        first_image = item.variant.variant_images.first()
        cart_data.append(
            {
                "name": item.variant.product.name,
                "price": item.variant.price,
                "size": item.variant.size,
                "image": first_image.image.url if first_image else "",
                "variant_id": item.variant.id,
                "quantity": item.quantity,
                "variant_type": item.variant.product.variant_type,
                "flavour": item.variant.flavour,
                "weight": item.variant.weight,
                "total_item_price": item.quantity * item.variant.price,
            }
        )

    return render(req, "cart_detail.html", {"cart_data": cart_data, "total": total})


@login_required
def add_to_cart(req, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)

    cart_item, created = CartItem.objects.get_or_create(
        variant=variant,
        user=req.user,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart:view_cart")


@login_required
@csrf_exempt
def update_to_cart(req):
    if req.method == "POST":
        quantity = req.POST.get("quantity")
        id = req.POST.get("id")
        size_id = req.POST.get("size_id")
        print(size_id, "----------")
        cart_item = CartItem.objects.get(variant_id=id)
        cart_item.quantity = cart_item.quantity + int(quantity)
        cart_item.save()
    if cart_item.quantity < 1:
        cart_item.quantity = 1
        cart_item.save()

    return redirect("cart:view_cart")


@login_required
def remove_from_cart(request, variant_id):
    cart_item = CartItem.objects.get(variant_id=variant_id)
    print(cart_item, "---------")
    cart_item.delete()

    return redirect("cart:view_cart")
