# Let's verify if the code compiles properly and identify any obvious logic issues.

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models import Count, Avg, Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import pandas as pd
import numpy as np
import time
import qrcode
import base64
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from django.db.models.functions import TruncDate
from .models import Transaction
from django.utils.timezone import now
import socket

# Assuming your models and serializers are correctly defined
from .models import Transaction, Product
from .serializers import TransactionSerializer

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def signup_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():
            return render(request, 'home.html', {'error': 'Email already exists'})
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        return redirect('home')

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'home.html', {'error': 'Invalid credentials'})

@api_view(['GET', 'POST'])
def transaction_api(request):
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_data(product_name, page=1, max_results=5):
    search_query = product_name.replace(" ", "+")
    url = f"https://www.amazon.com/s?k={search_query}&page={page}"
    driver = get_driver()
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all("a", class_="a-link-normal s-no-outline")
    links_list = ["https://www.amazon.com" + a.get('href') for a in links[:max_results]]

    data = {"title": [], "price": [], "rating": [], "reviews": [], "availability": [], "image": []}

    for link in links_list:
        try:
            driver.get(link)
            time.sleep(2)
            page = BeautifulSoup(driver.page_source, "html.parser")
            title = page.find("span", {"id": "productTitle"})
            data['title'].append(title.text.strip() if title else "")
            price = page.select_one(".a-price .a-offscreen")
            data['price'].append(price.text.strip() if price else "")
            rating = page.find("span", class_="a-icon-alt")
            data['rating'].append(rating.text.strip() if rating else "")
            reviews = page.find("span", {"id": "acrCustomerReviewText"})
            data['reviews'].append(reviews.text.strip() if reviews else "")
            availability = page.find("div", {"id": "availability"})
            available = availability.find("span").text.strip() if availability else "Not Available"
            data['availability'].append(available)
            image = page.find("div", {"id": "imgTagWrapperId"})
            if image and image.img:
                img_url = image.img.get("src")
                data['image'].append(img_url)
            else:
                data['image'].append("")
            if title and price:
                Product.objects.create(
                    name=title.text.strip(),
                    price=price.text.strip(),
                    rating=rating.text.strip() if rating else "",
                    reviews=reviews.text.strip() if reviews else "",
                    delivery=available
                )
        except Exception as e:
            print(f"Error scraping product: {e}")
            continue

    driver.quit()
    df = pd.DataFrame(data)
    df['title'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=['title'])

    def img_html(path):
        return f'<img src="{path}" width="100">'

    def add_to_cart_button(row):
        return f'''
        <form method="get" action="/payment/">
            <input type="hidden" name="product" value="{row['title']}">
            <input type="hidden" name="amount" value="{row['price'].replace('$', '')}">
            <input type="submit" value="Add to Cart 🛒">
        </form>
        '''

    df['cart'] = df.apply(add_to_cart_button, axis=1)

    return df.to_html(escape=False, formatters={'image': img_html, 'cart': lambda x: x})

def index(request):
    df_html = None
    product = request.GET.get('product') or request.POST.get('product')
    page = int(request.GET.get('page', 1))
    if product:
        df_html = get_data(product, page=page)
    return render(request, 'index.html', {
        'df': df_html,
        'product': product,
        'page': page,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1
    })



def get_client_ip(request):
    # Try to get the real IP if behind proxy
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def payment(request):
    if request.method == "POST":
        product = request.POST.get("product")
        amount = request.POST.get("amount")
        method = request.POST.get("method")
        result = None
        qr_image = None
        status_val = "Success"  # You can add real validation later
        ip = get_client_ip(request)

        if method == "card":
            card = request.POST.get("card")
            expiry = request.POST.get("expiry")
            cvv = request.POST.get("cvv")
            result = f"Payment of ₹{amount} via Card successful!"

            # 💾 Save transaction
            Transaction.objects.create(
                user=request.user.username if request.user.is_authenticated else "Guest",
                card_number=card,
                amount=amount,
                status=status_val,
                ip_address=ip
            )

        elif method == "upi":
            upi_id = request.POST.get("upi_id")
            result = f"Payment of ₹{amount} via UPI ({upi_id}) successful!"

            Transaction.objects.create(
                user=request.user.username if request.user.is_authenticated else "Guest",
                card_number="UPI:" + upi_id,
                amount=amount,
                status=status_val,
                ip_address=ip
            )

        elif method == "qr":
            upi_string = f"upi://pay?pa=sunakshi123@paytm&pn=Sunakshi&am={amount}&cu=INR"
            qr = qrcode.make(upi_string)
            buffered = BytesIO()
            qr.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            qr_image = f"data:image/png;base64,{img_str}"
            result = "Scan the QR code to complete the payment"

            Transaction.objects.create(
                user=request.user.username if request.user.is_authenticated else "Guest",
                card_number="QR",
                amount=amount,
                status=status_val,
                ip_address=ip
            )

        return render(request, 'payment.html', {
            'result': result,
            'qr_image': qr_image,
            'product': product,
            'amount': amount
        })
    return render(request, 'payment.html')