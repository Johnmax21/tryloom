from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.
def index(request):
    products = Product.objects.all()
    is_logged_in = 'email' in request.session

    return render(request, "index.html", {
        "products": products,
        "is_logged_in": is_logged_in
    })




# views.py

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Transaction, Wishlist, icart, user

@csrf_exempt  # Not recommended for production. Better: use {% csrf_token %} in the template.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        # Create and save user
        User = user(
            usernname=username,
            password=password,
            email=email,
            phone=phone,
            address=address,
            profile_picture=profile_picture
        )
        User.save()
        alert_message="<script>alert('User Created Successfully'); window.location.href='/login';</script>"
        return HttpResponse(alert_message)
        # return redirect('success')  # redirect to a success page

    return render(request, 'register.html')
# In views.py (optional)
from django.http import HttpResponse

def success(request):
    return HttpResponse("User created successfully!")
def adminlogin(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        password=request.POST.get('password')
        u='admin'
        p='123456'
        if uname==u:
            
            if password==p:
                return redirect('admin_dashboard')
            return render(request,'adminlogin.html')
    
        alert_message="<script>alert('INCORRECT EMAIL⚠️'); window.location.href='/adminlogin';</script>"
        return HttpResponse(alert_message)
    return render(request,'adminlogin.html')


def admin_dashboard(request):

    return render(request,'admin.html')




# views.py

from django.shortcuts import render, redirect
from .models import Product

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        stock = request.POST.get('stock')
        size = request.POST.get('size')
        color = request.POST.get('color')
        category = request.POST.get('category')
        offer_price = request.POST.get('offer_price') or None
        code = request.POST.get('code')
        fabric = request.POST.get('fabric')

        # Save product
        product = Product(
            name=name,
            description=description,
            price=price,
            image=image,
            stock=stock,
            size=size,
            color=color,
            category=category,
            offer_price=offer_price,
            code=code,
            fabric=fabric,
        )
        product.save()
        return redirect('admin_dashboard')  # or product list page

    return render(request, 'add_product.html')
def product_list(request):
    category = request.GET.get("category")
    sort = request.GET.get("sort")

    products = Product.objects.all()

    # Category filter
    if category:
        products = products.filter(category=category)

    # Sorting
    if sort == "low":
        products = products.order_by("price")
    elif sort == "high":
        products = products.order_by("-price")

    return render(request, "product_list.html", {"products": products})



def user_list(request):
    users = user.objects.all()
    return render(request, 'user_list.html', {'users': users})



from django.shortcuts import render, redirect
from .models import user  # Use lowercase if your model is actually called `user`
from django.urls import reverse

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email,"email")
        password = request.POST.get('password')

        try:
            user_obj = user.objects.get(email=email)
            if user_obj.password == password:
                # For demo purposes, we'll just redirect; implement session later
                request.session['email'] = email

                return redirect('index')  # You can define 'home' route separately
            else:
                return render(request, 'login.html', {'error': 'Invalid password.'})
        except Exception as w:
            print(w)
            return render(request, 'login.html', {'error': 'User does not exist.'})

    return render(request, 'login.html')
def home(request):
    return render(request, 'home.html') # Simple home page after login  # You can enhance this later with user-specific data            





from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import user
import random

# Store OTP temporarily in session

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user_obj = user.objects.get(email=email)
            otp = random.randint(100000, 999999)
            request.session['reset_email'] = email
            request.session['reset_otp'] = str(otp)

            # Send OTP via email
            send_mail(
                subject='Your OTP for Password Reset',
                message=f'Your OTP is {otp}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return redirect('verify_otp')
        except user.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': 'Email not found.'})
    return render(request, 'forgot_password.html')


def verify_otp_view(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        session_otp = request.session.get('reset_otp')

        if input_otp == session_otp:
            return redirect('reset_password')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'verify_otp.html')


def reset_password_view(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match.'})

        email = request.session.get('reset_email')
        try:
            user_obj = user.objects.get(email=email)
            user_obj.password = new_password  # ⚠️ Should hash this in real apps!
            user_obj.save()

            # Clean session
            request.session.pop('reset_email', None)
            request.session.pop('reset_otp', None)

            return redirect('login')
        except user.DoesNotExist:
            return render(request, 'reset_password.html', {'error': 'User not found.'})
    return render(request, 'reset_password.html')
from django.shortcuts import render
from .models import Product
def user_product_list(request):
    products = Product.objects.all().order_by('-created_at')
    user_wishlist = []

    user_email = request.session.get('email')
    if user_email:
        try:
            current_user = CustomUser.objects.get(email=user_email)
            user_wishlist = Wishlist.objects.filter(user=current_user).values_list('product_id', flat=True)
        except CustomUser.DoesNotExist:
            pass

    return render(request, 'user_product_list.html', {
        'products': products,
        'user_wishlist': user_wishlist,
    })







def cart_list(request):
    # Fetch the user's cart items
    if 'email' in request.session:
        email = request.session['email']
        juser = user.objects.get(email=email)
        print(juser)
        cart_items = icart.objects.filter(user=juser)

        return render(request, 'cart_list.html', {'cart_items': cart_items})
    else:
        return redirect('login')

def add_cart(request,pid):
    if 'email' in request.session:
        email=request.session.get('email')
        print(email,"email")
        us=user.objects.get(email=email)
        products=Product.objects.get(id=pid)
    
    
        
        

        if request.method == "POST":
            quantity = request.POST.get('quantity')
            quantity=int(quantity)
            total_price = Decimal(request.POST.get('total'))
            cart_item,created=icart.objects.get_or_create(user=us,products=products,defaults={'quantity':quantity,'total_price':total_price} )
            if not created:
                cart_item.quantity = quantity
                cart_item.total_price=total_price
           
                cart_item.save()

                return redirect('cart_list')
            return redirect('cart_list')
            
        else:
            return render(request,'cart.html',{'prd':products})
    else:
        return redirect('cart_list')
    



def delete_cart_item(request, id):
    
    cart_item = get_object_or_404(icart, id=id)
    cart_item.delete()
    return redirect('cart_list')
def wishlist_toggle(request, pid):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    email = request.session.get("email")
    if not email:
        return JsonResponse({"error": "Login required"}, status=403)

    userd = get_object_or_404(user, email=email)
    product = get_object_or_404(Product, id=pid)

    obj, created = Wishlist.objects.get_or_create(user=userd, product=product)

    if created:
        return JsonResponse({"in_wishlist": True, "message": "Added to wishlist"})

    obj.delete()
    return JsonResponse({"in_wishlist": False, "message": "Removed from wishlist"})


from django.shortcuts import render, get_object_or_404
from .models import Product, Review, Wishlist

def product_detail(request, pid):
    product = get_object_or_404(Product, id=pid)

    # --- Reviews ---
    reviews = Review.objects.filter(product=product)
    review_count = reviews.count()
    avg_rating = round(sum(r.rating for r in reviews) / review_count, 1) if review_count > 0 else 0

    # --- Wishlist check (IMPORTANT) ---
    in_wishlist = False
    email = request.session.get("email")

    if email:
        userd = get_object_or_404(user, email=email)
        in_wishlist = Wishlist.objects.filter(user=userd, product=product).exists()

    # --- Recently Viewed ---
    rv = request.session.get("recently_viewed", [])
    if pid not in rv:
        rv.insert(0, pid)
    rv = rv[:6]
    request.session["recently_viewed"] = rv

    recently_viewed_products = Product.objects.filter(id__in=rv)

    context = {
        "product": product,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "review_count": review_count,
        "recently_viewed": recently_viewed_products,
        "in_wishlist": in_wishlist,   #  <-- IMPORTANT
    }

    return render(request, "product_detail.html", context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Review
def add_review(request, pid):
    # Must be POST
    if request.method != "POST":
        return redirect("product_details", pid=pid)

    # Check login using SESSION
    user_email = request.session.get("email")
    if not user_email:
        messages.error(request, "Please login first.")
        return redirect("login")

    userd = get_object_or_404(user, email=user_email)
    product = get_object_or_404(Product, id=pid)

    # Get form data
    rating = request.POST.get("rating")
    comment = request.POST.get("comment")

    # Validation
    if not rating or not comment:
        messages.error(request, "Rating and comment required.")
        return redirect("product_details", pid=pid)

    # Check if review already exists (avoid UNIQUE constraint)
    existing_review = Review.objects.filter(product=product, user=userd).first()

    if existing_review:
        # Update existing review
        existing_review.rating = int(rating)
        existing_review.comment = comment
        existing_review.save()
        messages.success(request, "Review updated successfully!")
    else:
        # Create new review
        Review.objects.create(
            product=product,
            user=userd,
            rating=int(rating),
            comment=comment
        )
        messages.success(request, "Review submitted successfully!")

    return redirect("product_details", pid=pid)


from django.contrib.auth import logout
import razorpay # type: ignore
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
# from razorpay.errors import BadRequestError
from django.views.decorators.csrf import csrf_exempt

# from razorpay.errors import BadRequestError
from django.views.decorators.csrf import csrf_exempt




def initiate_payment(request,cid):
    email = request.session['email']
    if email:
        crt=icart.objects.get(id=cid)
        am=crt.total_price
        amount = int(am)*100 
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment_order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        order_id = payment_order['id']
        juser = user.objects.get(email=email)
        buyer_data = {
            'buyer': {
                'id': juser.id,
                'name': juser.usernname,
                'email': juser.email,
                'phone': juser.phone,
                # Add other fields as needed
            }
        }
        response_data = {'order_id': order_id, 'amount': amount}
        response_data.update(buyer_data)
        return JsonResponse(response_data, encoder=DjangoJSONEncoder)
    else:
        return redirect('log')
    

from decimal import Decimal   
@csrf_exempt
def confirm_payment(request, order_id, payment_id,crti_id):
    print('Confirm payment')
    try:
        print('Payment ID:', payment_id)
        print('order_id:', order_id)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.payment.fetch(payment_id)
        print('Payment:', payment['order_id'])
        print('payment', payment)
        if payment['order_id'] == order_id and payment['status'] == 'captured':
            pemail = payment.get('email')
            amount = payment.get('amount')
            amount_in_rupees = Decimal(amount) / Decimal(100)  

            if pemail:
                usr = user.objects.get(email=pemail)
                crts=icart.objects.get(id=crti_id)
             
                prd=crts.products
                trns=Transaction(user=usr,products=prd,amount=amount_in_rupees,quantity=crts.quantity,order_id=order_id)
                trns.save()
                crts.delete()
                return redirect('index')

            else:
               return JsonResponse({'status': 'failure', 'error': 'User email not found'})
        else:
            print(payment['status'])
            return JsonResponse({'status': 'failure', 'error': 'Payment status not captured'})
    except Exception as e:
        print('Error:', str(e))
        return redirect('index')
    



from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import icart, Product, user

def delete_cartlist(request, item_id):
    # Ensure user is logged in (session based)
    user_email = request.session.get("email")
    if not user_email:
        messages.error(request, "Please login first.")
        return redirect("login")

    userd = get_object_or_404(user, email=user_email)

    # Check if cart item exists and belongs to logged-in user
    item = get_object_or_404(icart, id=item_id, user=userd)

    item.delete()
    messages.success(request, "Item removed from cart.")

    return redirect("cart")   # <-- change to your cart page URL name
from django.shortcuts import render
from .models import Product
from django.db.models import Q

def search_products(request):
    query = request.GET.get("q", "")

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(color__icontains=query) |
        Q(size__icontains=query)
    ).distinct()

    context = {
        "products": products,
        "search_query": query,
    }
    return render(request, "product_list.html", context)
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import user

def profile_view(request):
       if 'email' in request.session:
        email = request.session['email']
        juser = user.objects.get(email=email) # For now: Assuming first user is logged-in
    # Replace with request.session / request.user later
   
        return render(request, "profile.html", {"profile": juser})
       return render(request, "index.html")



def update_profile(request):
    profile = user.objects.first()

    if request.method == "POST":
        profile.usernname = request.POST.get("usernname")
        profile.email = request.POST.get("email")
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")
        profile.gender = request.POST.get("gender")

        # Handle new image upload
        if "profile_picture" in request.FILES:
            img = request.FILES["profile_picture"]
            fs = FileSystemStorage()
            filename = fs.save(img.name, img)
            uploaded_url = fs.url(filename)
            profile.profile_picture = filename

        profile.save()
        return redirect("profile")

    return render(request, "profile.html", {"profile": profile})


from django.shortcuts import render, redirect
from .models import Wishlist

def wishlist_page(request):
    if "email" not in request.session:
        return redirect("login")

    user_email = request.session["email"]

    wishlist_items = Wishlist.objects.filter(
        user__email=user_email
    ).select_related("product")

    return render(request, "wishlist.html", {
        "wishlist_items": wishlist_items,
    })
from django.shortcuts import redirect

def logout_view(request):
    if 'email' in request.session:
        del request.session['email']   # remove session email
    request.session.flush()            # clears all session data
    return redirect('index')               # redirect to home page
