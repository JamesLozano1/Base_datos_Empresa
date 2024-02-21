from django import forms
from .models import Producto_Proteccion, Producto_almacen, RetiroProducto

class FormsProducto_Proteccion(forms.ModelForm):
    class Meta:
        model = Producto_Proteccion
        fields = '__all__'
    
class FormsProducto_almacen(forms.ModelForm):
    class Meta:
        model = Producto_almacen
        fields = '__all__'

class FormsRetiroProductos(forms.ModelForm):
    class Meta:
        model = RetiroProducto
        fields = ['nombre_persona', 'cantidad_retirada']