from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from .models import Fertilizer
from .forms import *
from .forms import UserRegistrationForm  # Import the form
from .forms import userloginForm  # Corrected import
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Crop, SoilType


from .models import Fertilizer
def home(request):
    query = request.GET.get('q', '')
    fertilizers = Fertilizer.objects.all()
    scroll_to_id = None

    if query:
        fertilizers = Fertilizer.objects.filter(name__icontains=query)
        if fertilizers.exists():
            scroll_to_id = fertilizers.first().id  # Get the ID of the first matching fertilizer

    return render(request, 'home.html', {'fertilizers': fertilizers, 'scroll_to_id': scroll_to_id})


def user_login(request):
    if request.method == 'POST':
        form = userloginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect(reverse('admin_dashboard'))
                else:
                    return redirect(reverse('dashboard'))
            
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = userloginForm()
    return render(request, 'login.html', {'form': form})

def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')

    # Calculate totals
    total_fertilizers = Fertilizer.objects.count()
    total_crops = Crop.objects.count()
    total_soil_types = SoilType.objects.count()
    total_sales = Sale.objects.count()

    # Pass totals to the template
    context = {
        'total_fertilizers': total_fertilizers,
        'total_crops': total_crops,
        'total_soil_types': total_soil_types,
        'total_sales': total_sales,
    }
    return render(request, 'admin_dashboard.html', context)
        
from django.shortcuts import render
from .models import Fertilizer

def dashboard(request):
    query = request.GET.get('search', '')  # Get the search query from the request
    if query:
        fertilizers = Fertilizer.objects.filter(name__icontains=query)  # Filter fertilizers by name
    else:
        fertilizers = Fertilizer.objects.all()  # Display all fertilizers if no query
    return render(request, 'dashboard.html', {'fertilizers': fertilizers, 'query': query})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()  # Define the form
    return render(request, 'register.html', {'form': form}) 


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def fertilizer_list(request):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('user_login'))
            fertilizers = Fertilizer.objects.all()
            return render(request, 'fertilizer_list.html', {'fertilizers': fertilizers})

def fertilizer_detail(request, pk):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('user_login'))
            fertilizer = Fertilizer.objects.get(pk=pk)
            return render(request, 'fertilizer_detail.html', {'fertilizer': fertilizer})

def fertilizer_create(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = FertilizerForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('fertilizer_list')
    else:
        form = FertilizerForm()
    return render(request, 'fertilizer_form.html', {'form': form})

def fertilizer_update(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))
    fertilizer = Fertilizer.objects.get(pk=pk)
    if request.method == 'POST':
        form = FertilizerForm(request.POST, instance=fertilizer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('fertilizer_list'))
    else:
        form = FertilizerForm(instance=fertilizer)
    return render(request, 'fertilizer_form.html', {'form': form})

def fertilizer_delete(request, pk):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('user_login'))
            fertilizer = Fertilizer.objects.get(pk=pk)
            if request.method == 'POST':
                fertilizer.delete()
                return HttpResponseRedirect(reverse('fertilizer_list'))
            return render(request, 'fertilizer_confirm_delete.html', {'fertilizer': fertilizer})


from django.shortcuts import render, redirect
from .forms import SoilTypeForm

def soiltype_form(request):
    if request.method == 'POST':
        form = SoilTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('soiltype_list')  # Redirect to the soil type list view
    else:
        form = SoilTypeForm()
    return render(request, 'soiltype_form.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import SoilType
from .forms import SoilTypeForm

# List View
def soiltype_list(request):
    soil_types = SoilType.objects.all()
    return render(request, 'soiltype_list.html', {'soil_types': soil_types})

# Create View
def soiltype_create(request):
    if request.method == 'POST':
        form = SoilTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('soiltype_list')
    else:
        form = SoilTypeForm()
    return render(request, 'soiltype_form.html', {'form': form})

# Update View
def soiltype_update(request, pk):
    soil_type = get_object_or_404(SoilType, pk=pk)
    if request.method == 'POST':
        form = SoilTypeForm(request.POST, instance=soil_type)
        if form.is_valid():
            form.save()
            return redirect('soiltype_list')
    else:
        form = SoilTypeForm(instance=soil_type)
    return render(request, 'soiltype_form.html', {'form': form})

# Delete View
def soiltype_delete(request, pk):
    soil_type = get_object_or_404(SoilType, pk=pk)
    if request.method == 'POST':
        soil_type.delete()
        return redirect('soiltype_list')
    return render(request, 'soiltype_confirm_delete.html', {'soil_type': soil_type})

from django.shortcuts import render, redirect
from .forms import CropForm

def crop_form(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crop_list')  # Redirect to the crop list view
    else:
        form = CropForm()
    return render(request, 'crop_form.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Crop
from .forms import CropForm

# List View
def crop_list(request):
    crops = Crop.objects.all()
    return render(request, 'crop_list.html', {'crops': crops})

# Create View
def crop_create(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crop_list')
    else:
        form = CropForm()
    return render(request, 'crop_form.html', {'form': form})

# Update View
def crop_update(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('crop_list')
    else:
        form = CropForm(instance=crop)
    return render(request, 'crop_form.html', {'form': form})

# Delete View
def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == 'POST':
        crop.delete()
        return redirect('crop_list')
    return render(request, 'crop_confirm_delete.html', {'crop': crop})

from django.shortcuts import render, get_object_or_404, redirect


from .models import Recommendation
from .forms import RecommendationForm

# List View
def recommendation_list(request):
    recommendations = Recommendation.objects.all()
    return render(request, 'recommendation_list.html', {'recommendations': recommendations})

# Create View
def recommendation_create(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recommendation_list')
    else:
        form = RecommendationForm()
    return render(request, 'recommendation_form.html', {'form': form})

# Update View
def recommendation_update(request, pk):
    recommendation = get_object_or_404(Recommendation, pk=pk)
    if request.method == 'POST':
        form = RecommendationForm(request.POST, instance=recommendation)
        if form.is_valid():
            form.save()
            return redirect('recommendation_list')
    else:
        form = RecommendationForm(instance=recommendation)
    return render(request, 'recommendation_form.html', {'form': form})

def recommendation_delete(request, pk):
    recommendation = get_object_or_404(Recommendation, pk=pk)
    if request.method == 'POST':
        recommendation.delete()
        return redirect('recommendation_list')
    return render(request, 'recommendation_confirm_delete.html', {'recommendation': recommendation})

from django.shortcuts import render, get_object_or_404

def recommendation_detail(request, pk):
    recommendation = get_object_or_404(Recommendation, pk=pk)
    return render(request, 'recommendation_detail.html', {'recommendation': recommendation})

from django.shortcuts import render
from .models import Recommendation, SoilType, Crop

def get_recommendation(request):
    recommendations = None
    if request.method == 'POST':
        soil_type_id = request.POST.get('soil_type')
        crop_id = request.POST.get('crop')
        soil_type = SoilType.objects.get(id=soil_type_id)
        crop = Crop.objects.get(id=crop_id)
        recommendations = Recommendation.objects.filter(soil_type=soil_type, crop=crop)
    soil_types = SoilType.objects.all()
    crops = Crop.objects.all()
    return render(request, 'get_recommendation.html', {
        'soil_types': soil_types,
        'crops': crops,
        'recommendations': recommendations
    })


from django.shortcuts import render, redirect
from .models import Sale
from django.db.models import Q, F, ExpressionWrapper, DecimalField, Sum, Count
from datetime import datetime

def sales_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')

    sales = Sale.objects.all()
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    sort_by = request.GET.get('sort_by')
    search_query = request.GET.get('search_query', '')

    # Annotate for sorting by total_price at the database level
    sales = sales.annotate(
        db_total_price=ExpressionWrapper(
            F('quantity_sold') * F('unit_price'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    start_date = None
    end_date = None

    if start_date_str:
        try:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            sales = sales.filter(date__gte=start_date)
        except ValueError:
            start_date = None

    if end_date_str:
        try:
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            sales = sales.filter(date__lte=end_date)
        except ValueError:
            end_date = None

    if search_query:
        sales = sales.filter(
            Q(farmer_name__icontains=search_query) |
            Q(aadhar_number__icontains=search_query) |
            Q(fertilizer__name__icontains=search_query)
        )

    # Apply sorting
    if sort_by == 'total_price':
        sales = sales.order_by('db_total_price')
    elif sort_by == '-total_price':
        sales = sales.order_by('-db_total_price')
    elif sort_by: # For 'date' or '-date' or any other valid field
        sales = sales.order_by(sort_by)
    else: # Default sort
        sales = sales.order_by('-date')

    # Evaluate queryset to list to use model properties for sum, after all filtering and sorting
    sales_list = list(sales)

    # Calculate totals using Python sum on model properties
    total_sales_amount = sum(s.total_price for s in sales_list) if sales_list else 0
    total_due_amount = sum(s.balance_due for s in sales_list) if sales_list else 0
    total_orders_count = len(sales_list)

    context = {
        'sales': sales_list, # Pass the evaluated list to the template
        'total_sales': total_sales_amount,
        'total_due': total_due_amount,
        'total_orders': total_orders_count,
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query,
        'current_sort': sort_by
    }
    return render(request, 'cemapp/sales_dashboard.html', context)

from .models import Fertilizer
from django.db.models import F

def low_stock_alert(request):
    low_stock_items = Fertilizer.objects.filter(quantity__lte=F('minimum_stock'))
    return render(request, 'cemapp/low_stock_alert.html', {'low_stock_items': low_stock_items})

from .forms import SaleForm

def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_dashboard')
    else:
        form = SaleForm()
    return render(request, 'cemapp/add_sale.html', {'form': form})

from django.shortcuts import get_object_or_404, render, redirect
from .models import Sale
from .forms import PaymentForm

def add_payment(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.sale = sale
            payment.save()
            return redirect('sales_dashboard')  # Redirect to the sales dashboard
    else:
        form = PaymentForm()
    return render(request, 'cemapp/add_payment.html', {'form': form, 'sale': sale})

def get_fertilizer_quantity(request, fertilizer_id):
    try:
        fertilizer = Fertilizer.objects.get(id=fertilizer_id)
        return JsonResponse({'quantity': fertilizer.quantity})
    except Fertilizer.DoesNotExist:
        return JsonResponse({'error': 'Fertilizer not found'}, status=404)
    

from django.shortcuts import render

def contact(request):
    return render(request, 'contact.html')


from django.shortcuts import render

def features(request):
    return render(request, 'features.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Update user details
        user = request.user
        user.username = username
        user.email = email
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard')

    return render(request, 'edit_profile.html', {'user': request.user})