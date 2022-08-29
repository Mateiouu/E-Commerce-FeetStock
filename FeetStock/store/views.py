from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
import json
from .forms import ProductoFormulario
import datetime
from django.views.generic import CreateView
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
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

# def cart(request):
# 	try:
# 		customer = request.user.customer
# 	except:
# 		device = request.COOKIES['device']
# 		customer, created = Customer.objects.get_or_create(device=device)

# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)

# 	context = {'order':order}
# 	return render(request, 'store/cart.html', context)
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

# def eliminaritem(request, id):
#     if request.method == "POST":
         
        

#         item = OrderItem.objects.get(product = id)
#         item.delete()
#         return render(request, "store/deletecartitem.html", {'item': item})

#     if  OrderItem.objects.all == None:
#         customer =   customer = request.user.customer
#         order = Order.objects.all(customer = customer)
#         order.delete()


# @login_required
# @require_http_methods(['DELETE', 'POST'])
# def eliminaritem(request, id):
#     order_items = OrderItem.objects.filter(
#         order__complete=False, order__customer__user=request.user
#     )
#     item = get_object_or_404(order_items, product_id=id)
#     item.delete()
#     if not order_items.exists():
#         Order.objects.filter(
#             customer__user=request.user, complete=False
#         ).delete()
#     return render(request, 'store/deletecartitem.html')

def eliminaritem(request, id):
    if request.method == "POST":
        item = OrderItem.objects.get(product = id)

      
        relevant_order = item.order

        
        if not relevant_order.customer == request.user:
            
            item.delete()

       
        if not relevant_order.orderitem_set.all():
            relevant_order.delete()

    return render(request, "store/deletecartitem.html")



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = OrderItem.objects.get_or_create(customer = customer, complete = False)

    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1 )

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()



    # return JsonResponse('Item was added', safe = False)

def loginView(request):
    if request.method =='POST':
           miFormulario=AuthenticationForm(request, data=request.POST)#aquí mellega toda la información del html
           

           if miFormulario.is_valid():#Si pasó la validación de Django
                data=miFormulario.cleaned_data

                usuario = data['username']
                psw = data['password']
               
                user = authenticate(username=usuario, password=psw)
                if user:
                    login(request,user)
                    return render(request, 'store/homee.html', {'mensaje': f'Bienvenido {usuario}'})
                
                else:

                    return render(request, 'store/homee.html', {'mensaje': 'No se ha podido iniciar sesion, revise sus datos'})
           return render(request, 'store/homee.html', {'mensaje': 'Formulario invalido'})
    else:
        miFormulario=AuthenticationForm()

    return render(request, 'store/login.html', {'miFormulario': miFormulario})

def registerView(request):
   
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            context = {'form': form}
            return render(request, 'store/homee.html', context)
    else:

        form = CreateUserForm()

    return render(request, 'store/register.html', {'form': form})
   

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


class CambiarContraView(PasswordChangeView):
    from_class = PasswordChangeForm
    success_url = reverse_lazy('login')



class ProductoCreate(CreateView):
    model = Product
    fields = ["name", "price","sex", "image"]
    success_url = '/tienda'
    template_name = 'storeproduct_create.html'
 

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

# @staff_member_required
# def crearproducto(request):
#      if request.method =='POST':
#            miFormularioA=ProductoFormulario(request.POST)
#            print(miFormularioA)

#            if miFormularioA.is_valid:
#                  informacion=miFormularioA.cleaned_data
#                  producto=Product(name=informacion['name'],sex=informacion['sex'], price=informacion['price'], image=informacion['image'])
#                  producto.save()
#                  return render(request,"inicio.html")
#      else:      
#            miFormularioA=ProductoFormulario()
#            return render(request,"store/crearproducto.html",{"miFormularioA":miFormularioA})

    


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



