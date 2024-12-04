from django.shortcuts import render, redirect
from django.http import  HttpResponse 
from rest_framework.decorators import api_view, renderer_classes,permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from django.views.decorators.csrf import csrf_exempt
from  .models import  MenuItems,  Order, Cart, Category
from .serializer import MenuSerializer,  CartSerializer, CategorySerializer,OrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response 
from rest_framework import viewsets 
#permisos
from rest_framework.permissions import IsAuthenticated, IsAdminUser,  AllowAny
from django.contrib.auth import authenticate, login as auth_login
from .throttle import TenCallPerMinute
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


        
def inde(request):
    if request.method == 'GET':
        return render(request, "next/index.html")
    
#Login Inciar Seccion
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponse('Login exitoso')
        
        else:
            return HttpResponse('Error de credenciales')
    return render(request, "next/index.html")

#from .models import MenuItems
#from .serializers import MenuItemSerializer  

class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuSerializer
    ordering_fields=['price','inventory']
    search_fields=['title','category__title']
    

@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)

#login
@api_view(['POST','GET'])
@permission_classes([IsAdminUser])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'message': 'Ingrese Su Usuario Y Contraseña'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return Response({'message': 'Ingreso Con Exito'}, status=status.HTTP_200_OK)
    return Response({'message': 'Incorrecto Digite Nuevamente Su Usuario Y contraseña'}, status=status.HTTP_401_UNAUTHORIZED)  



@api_view(['GET', 'POST'])
def menu_item(request):
    if request.method == 'GET':
        item = MenuItems.objects.select_related('category').all()
        #componetes de filtracion
        category_name = request.query_params.get('category')#filtrar datos
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        
        #paginacion
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            item = item.filter(category__title=category_name)
            if to_price:
                item = item.filter(price=to_price)
        # busqueda 
        if search:
            item = item.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            item = item.order_by(*ordering_fields)
        # paginacion
        paginator = Paginator(item, per_page=perpage)
        try:
            item = paginator.page(page)
        except EmptyPage:
            item = paginator.page(paginator.num_pages)

        serializer_item = MenuSerializer(item , many=True, context={'request': request})
        return  Response(serializer_item.data)
    
    if request.method == 'POST':
        serializer = MenuSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            # validar los datos de post
            serializer.save()   #guardamos 
            return Response(serializer.data, status.HTTP_201_CREATED)    
        return Response(serializer.errors, status.HTTP_404_NOT_FOUND)

#INDICE DE MENU EXISTENTE
@api_view()   
@permission_classes(IsAuthenticated)
def SingleItem(request, id):
    item = get_object_or_404(MenuItems, pk=id)
    serializer_item = MenuSerializer(item)
    return Response(serializer_item.data)

#categoria
@api_view(['GET', 'POST'])
def categorytoo(request):
    if request.method == 'GET':
        category = Category.objects.all()
        serializer_category = CategorySerializer(category, many=True, context={'request': request})
        return Response(serializer_category.data)
    
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
    @get_permissions()
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
#cotegoryid
@api_view(['GET'])
def categoryid(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer_category = CategorySerializer(category, context={'request': request})
    return Response(serializer_category.data)

#______________________________________________________________________________________
#TODA ESTA SECCION TIENE INCLUEDO EL SISTEMA DE JWT
#token permiso
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token:
        return Response({'message': 'Authorized'}, status.HTTP_200_OK)
    return Response({'message': 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)
#Funciones de los Gerentes
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    #verificar si el usuario es admin
    if request.user.groups.filter(name='manager').exists():
        return Response({'message': 'El gerente autorizado solo debe ver esto'}, status.HTTP_200_OK)
    return Response({'message': 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)
#tiempo
@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallPerMinute])
def throtte_check_auth(request):
    #tiempo de espera
    return Response({"menssage":'mensage for logged in user only'})
    
@api_view()
@permission_classes([IsAuthenticated]) 
def me(request):
    return Response(request.user.email)        
#perfil
@api_view(['POST'])
@permission_classes([IsAdminUser])
def manager(request):
    #verificar si el usuario es admin
    return Response({'massage':"ok"})
#_________________________________________________________________________________________

#@api_view(['GET','POST'])
#def UserViewtoo(request):
 #   if request.method == 'GET':
  #      users = userview.objects.all()
   #     serializer = UserSerializer(users, many=True)
    #    return Response(serializer.data)
    #elif request.method == 'POST':
     #   serializer = UserSerializer(data=request.data)
      ##  if serializer.is_valid():
        #    serializer.save()
         #   return Response(serializer.data, status=status.HTTP_201_CREATED)
    #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#SECCION DE COMPRAS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    serializer = CartSerializer(cart, many=True)
    return Response(serializer.data)


#SECCIOPN DE PEDIR 
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def order(request):
    if request.method == 'GET':
        orders = Order.objects.all().select_related('related_model')  # Optimiza la consulta si hay relaciones
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#SECCION DE CANTIDAD DE ORDE
@api_view()
def orderpk(request, pk):
    try:
        order = get_object_or_404(Order,pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    


