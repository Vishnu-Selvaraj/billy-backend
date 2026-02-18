from django.urls import path
from . import views

urlpatterns = [
    path('createUser',views.addUser,name='addUser'),
    path('getAllUsers',views.getAllUsers,name='getAllUsers'),
    path('addProduct',views.createProduct,name='create_product'),
    path('getAllProducts',views.getAllProducts,name='getAllProducts'),
    path('addInvoice',views.create_invoice,name='addInvoice'),
    path('getAllInvoices',views.getAllInvoices,name='getAllInvoices'),
    path('getAllInvoiceById/<invoice_id>',views.getInvoiceById,name='getInvoiceById'),
]
