from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns =[
    path("index/", views.inde, name="index" ),
    path('menu/', views.menu_item, name="menu"),
    path('menu/<int:id>/', views.SingleItem),
    #path('welcome/', views.welcome),
    path('login/', views.login),
    path('menu-items',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu-items/<int:pk>',views.MenuItemsViewSet.as_view({'get':'retrieve'})),
    path('categorytoo/', views.categorytoo),
    path('categorytoo/<int:pk>', views.categoryid),
    path('order/', views.order),
    path('order/<int:pk>',views.orderpk),
    path('cart/', views.cart),
    #________________________________________________________#
    path('secret/',  views.secret, name="secret"),
    path('api-token-auth/', obtain_auth_token),
    path('manager-view/', views.manager_view),
    path('thrortte/', views.throtte_check_auth),
    path('me/', views.me),
    path('manager/', views.manager),
    #path('user-view/', views.UserViewtoo),
  
    
    
    
]