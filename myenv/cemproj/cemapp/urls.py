from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('fertilizer/create/', views.fertilizer_create, name='fertilizer_create'),
    path('fertilizer/', views.fertilizer_list, name='fertilizer_list'),
    path('fertilizer/<int:pk>/update/', views.fertilizer_update, name='fertilizer_update'),
    path('fertilizer/<int:pk>/delete/', views.fertilizer_delete, name='fertilizer_delete'),
    path('fertilizer/<int:pk>/', views.fertilizer_detail, name='fertilizer_detail'),    
    path('password-reset/', PasswordResetView.as_view(template_name='password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    path('soiltype/form/', views.soiltype_form, name='soiltype_form'),
    path('soiltype/', views.soiltype_list, name='soiltype_list'),
    path('soiltype/create/', views.soiltype_create, name='soiltype_create'),
    path('soiltype/update/<int:pk>/', views.soiltype_update, name='soiltype_update'),
    path('soiltype/delete/<int:pk>/', views.soiltype_delete, name='soiltype_delete'),
    path('crop/form/', views.crop_form, name='crop_form'),
    path('crop/', views.crop_list, name='crop_list'),
    path('crop/create/', views.crop_create, name='crop_create'),
    path('crop/update/<int:pk>/', views.crop_update, name='crop_update'),
    path('crop/delete/<int:pk>/', views.crop_delete, name='crop_delete'),
    path('recommendations/', views.recommendation_list, name='recommendation_list'),
    path('recommendations/create/', views.recommendation_create, name='recommendation_create'),
    path('recommendations/update/<int:pk>/', views.recommendation_update, name='recommendation_update'),
    path('recommendations/delete/<int:pk>/', views.recommendation_delete, name='recommendation_delete'),
    path('recommendations/<int:pk>/', views.recommendation_detail, name='recommendation_detail'),
    path('get-recommendation/', views.get_recommendation, name='get_recommendation'),

    path('sales/', views.sales_dashboard, name='sales_dashboard'),
    path('sales/add/', views.add_sale, name='add_sale'),
    path('alerts/low-stock/', views.low_stock_alert, name='low_stock_alert'),
    path('payments/add/<int:sale_id>/', views.add_payment, name='add_payment'),
    path('get_fertilizer_quantity/<int:fertilizer_id>/', views.get_fertilizer_quantity, name='get_fertilizer_quantity'),

    path('contact/', views.contact, name='contact'), 

    path('features/', views.features, name='features'), 
    path('edit-profile/', views.edit_profile, name='edit_profile'),  
    ]

