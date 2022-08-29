
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .forms import ProductoFormulario
import datetime
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

# Create your views here.
def home(request):
    return render(request,'store/homee.html')

def about(request):
    return render(request,'store/about.html')
# @staff_member_required(login_url = '/login')



def store(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'store/store.html', context)

def product(request, pk):
	product = Product.objects.get(id=pk)

	if request.method == 'POST':
		product = Product.objects.get(id=pk)
		#Get user account information
		try:
			customer = request.user.customer	
		except:
			device = request.COOKIES['device']
			customer, created = Customer.objects.get_or_create(device=device)

		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
		orderItem.quantity=request.POST['quantity']
		orderItem.save()

		return redirect('cart')

	context = {'product':product}
	return render(request, 'store/product.html', context)


@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

         
        

def eliminaritem(request, id):
   
    if request.method == "POST":
        item = OrderItem.objects.get(product = id)

      
        relevant_order = item.order

        
        if not relevant_order.customer == request.user:
            
            item.delete()

       
        if not relevant_order.orderitem_set.all():
            relevant_order.delete()
        
        order =  Order.objects.all()
        context = {'order':order}


    return render(request, "store/deletecartitem.html" , context)








def hombre(request):
    products = Product.objects.all()
    contexto = {'products':products}
    return render(request,'store/hombre.html', contexto)

def mujer(request):
    products = Product.objects.all()
    contexto = {'products':products}
    return render(request,'store/mujer.html', contexto)

def ninio(request):
    products = Product.objects.all()
    contexto = {'products':products}
    return render(request,'store/ninio.html', contexto)






 

class ProductoUpdate(UpdateView):
    model = Product
    fields = ["name", "price","sex", "image"]
    template_name = 'store/product_update.html'
    success_url = '/tienda/'
   

class ProductoDelete(DeleteView):
    model = Product
    template_name = 'store/product_delete.html'
    success_url = '/tienda/'

class ProductoCreate(CreateView):
    model = Product
    fields = ["name", "price", "sex", "image"]
    template_name = 'store/product_create.html'
    success_url = '/tienda/'

def agregarproducto(request):
    form = ProductoFormulario
    if request.method =='POST':
     form= ProductoFormulario(request.POST, request.FILES['image'])
    
     form.save()
        

    context = {'form': form}
    return render(request, 'store/product_create.html', context)




def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        
        order.transaction_id = transaction_id
        if True:
            order.complete = True
        order.save()
    return render(request, 'store/payment.html')

def nohaycontenido(request):
    return  render(request, 'store/nohaycontenido.html')



