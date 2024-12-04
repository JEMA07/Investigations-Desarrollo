from django.db import models
from django.contrib.auth.models import User
# Create your models here.




# LENEA DE RESTAURANTES
class Restaurantes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"
        
    def __str__(self):
        return self.nombre
# CATEGORIA
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=250)
    
    
    def __str__(self):
        return   self.title 
# SECCION MENU
class MenuItems(models.Model):
    title = models.CharField(max_length=250, db_index=True)
    price = models.DecimalField(max_digits=3, decimal_places=2)   
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    inventory = models.IntegerField()
    featured = models.BooleanField(db_index=True)   
    def __str__(self) -> str:
       return  self.title  


        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2)
    shcreated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (['menu'])
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    def __str__(self):
        return f"Order id : {self.id}, Quien Ordena: {self.user}"
    
    def save(self, *args, **kwargs):
        self.total = self.cart.total
        super(Order, self).save(*args, **kwargs)

#CARRITO DE COMPRA
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=6, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, 
                              choices=[('pending', 'Pending'),
                                       ('shipped', 'Shipped'),
                                       ('completed', 'Completed'),])
    
    class Meta:
        unique_together = (['user'])
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        
    def __str__(self):
        return f"Cart id: {self.id}, User: {self.user}, Menu Item: {self.menuitem}, Category: {self.category}"
    def save(self, *args, **kwargs):
        self.total = (self.orden.price * self.quantity)
        super(Cart, self).save(*args, **kwargs)
    
      
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2)
    class Meta:
        unique_together =('order','menuitem')
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
       
    
##class userview(models.Model):
  #  username = models.CharField(max_length=255, unique=True)
   # email = models.EmailField(unique=True)
    #password = models.CharField(max_length=255, default='123')
    # password = models.CharField(max_length=255, default='123')
