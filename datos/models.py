from django.db import models

class Producto_Proteccion(models.Model):
    nombre = models.CharField(max_length=150)
    cantidad_disponible  = models.PositiveBigIntegerField()
    imagen = models.ImageField()

    def __str__( self ):
        return self.nombre

class Producto_almacen(models.Model):
    nombre = models.CharField(max_length=150)
    cantidad_disponible  = models.PositiveBigIntegerField()
    imagen = models.ImageField()

    def __str__( self ):
        return self.nombre
    

class RetiroProducto(models.Model):
    producto_proteccion = models.ForeignKey(Producto_Proteccion, on_delete=models.SET_NULL, null=True, blank=True)
    producto_almacen = models.ForeignKey(Producto_almacen, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_persona = models.CharField(max_length=255)
    cantidad_retirada = models.PositiveIntegerField()
    fecha_retiro = models.DateTimeField(auto_now_add=True)



    def __str__( self ):
        return f"{self.nombre_persona} {self.fecha_retiro.day}"