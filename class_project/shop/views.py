from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, CartItem, Category
from django.db.models import F, Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import json

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')

    if category_slug:
        if category_slug == 'clothing':
            products = products.filter(
                Q(name__icontains='running') |
                Q(name__icontains='shorts') |
                Q(name__icontains='sports') |
                Q(name__icontains='cap') |
                Q(name__icontains='t-shirt') |
                Q(name__icontains='tshirt') |
                Q(name__icontains='hoodie') |
                Q(name__icontains='jacket') |
                Q(name__icontains='trench') |
                Q(name__icontains='jeans') |
                Q(name__icontains='shirt') |
                Q(name__icontains='pants')
            )
        elif category_slug == 'accessories':
            products = products.filter(
                Q(name__icontains='graphic') |
                Q(name__icontains='tee') |
                Q(name__icontains='beanie') |
                Q(name__icontains='hat') |
                Q(name__icontains='sunglasses') |
                Q(name__icontains='scarf') |
                Q(name__icontains='gloves') |
                Q(name__icontains='belt') |
                Q(name__icontains='watch') |
                Q(name__icontains='wallet')
            )
        elif category_slug == 'footwear':
            products = products.filter(
                Q(name__icontains='slides') |
                Q(name__icontains='sneakers') |
                Q(name__icontains='shoes')
            )
        elif category_slug == 'bag':
            products = products.filter(
                Q(name__icontains='backpack') |
                Q(name__icontains='bag')
            )
        else:
            products = products.filter(category__slug=category_slug)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Debug print
    print(f"Category: {category_slug}")
    print(f"Number of products: {products.count()}")
    for product in products:
        print(f"Product: {product.name}")

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query
    })

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'count': sum(item.quantity for item in cart_items)
        })
        
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity = F('quantity') + 1
            cart_item.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'increase':
                cart_item.quantity = F('quantity') + 1
                cart_item.save()
            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity = F('quantity') - 1
                    cart_item.save()
                else:
                    cart_item.delete()
            
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def checkout(request):
    if request.method == 'POST':
        # Clear the user's cart
        CartItem.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def search(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'products': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )[:5]  # Limit to 5 results for live search
    
    results = [{
        'name': product.name,
        'price': str(product.price),
        'image': product.image.url if product.image else '',
    } for product in products]
    
    return JsonResponse({'products': results})
