from django.urls import path
from . import views

app_name= 'invoice'

urlpatterns = [
    path('add_customer', views.add_customer, name="add_customer"),
    path('add_invoice', views.add_invoice, name="add_invoice"),
    path('invoices/<int:customer_id>/',views.view_invoices, name='view_invoices'),
    path('customers', views.view_customers, name='view_customers'),
    path('user_invoices', views.view_user_invoices, name='view_user_invoices'),
    path('update_invoice/<int:pk>/', views.update_invoice, name='update_invoice'),
    path('update_customer/<int:pk>/', views.update_customer, name='update_customer'),
    path('customer/delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('invoice/delete/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('generate-receipt-pdf/<str:invoice_number>/', views.generate_receipt_pdf, name='generate_receipt_pdf'),
    path('receipt', views.receipt, name='receipt'),

]