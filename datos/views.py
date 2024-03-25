from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto_Proteccion, Producto_almacen,RetiroProducto
from .forms import FormsProducto_Proteccion, FormsProducto_almacen, FormsRetiroProductos
from collections import Counter
from django.db.models import Q
import subprocess
from django.http import HttpResponse
from datetime import datetime



def inicio(request):
    titulo = "Pago de $ 60.000"

    return render(request, 'index.html', {
        'titulo':titulo,
    })

def Agregar_Producto_Proteccion(request):
    if request.method == 'POST':
        form = FormsProducto_Proteccion(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos_Proteccion')

    else:
        form = FormsProducto_Proteccion()
    return render(request, 'Proteccion/Añadir_Producto_Proteccion.html',{
        'form': form,
    })

def Agregar_Producto_Almacen(request):
    if request.method == 'POST':
        form = FormsProducto_almacen(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos_Almacen')
    else:
        form = FormsProducto_almacen()
    return render(request, 'Almacen/Añadir_Producto_Almacen.html',{
        'form': form,
    })




def productos_Almacen(request):
    productos = Producto_almacen.objects.all()
    return render(request, 'Almacen/productos_Almacen.html', {
        'productos':productos,
    })

def productos_Proteccion(request):
    productos = Producto_Proteccion.objects.all()
    return render(request, 'Proteccion/productos_Proteccion.html', {
        'productos':productos,
    })

# def buscar_producto_proteccion(request):
#     query = request.GET.get('q', '')
#     Proteccion = Producto_Proteccion.objects.filter(nombre__icontains=query)
#     return render(request, 'Proteccion/productos_Proteccion.html', {
#         'Proteccion':Proteccion,
#     })

# def buscar_producto_almacen(request):
#     query = request.GET.get('q', '')
#     Almacen = Producto_almacen.objects.filter(nombre__icontains=query)
#     return render(request, 'Almacen/productos_Almacen.html', {
#         'Almacen': Almacen,
#     })

def buscar_productos(request):
    query = request.GET.get('q', '')

    resultados_proteccion = Producto_Proteccion.objects.filter(
        Q(nombre__icontains=query)
    )

    resultados_almacen = Producto_almacen.objects.filter(
        Q(nombre__icontains=query)
    )

    return render(request, 'busqueda_resultados.html', {
        'resultados_proteccion': resultados_proteccion,
        'resultados_almacen': resultados_almacen,
        'query': query,
    })

def editar_producto_Proteccion(request, producto_id):
    producto = get_object_or_404(Producto_Proteccion, pk=producto_id)

    if request.method == 'POST':
        form = FormsProducto_Proteccion(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos_Proteccion')  
    else:
        form = FormsProducto_Proteccion(instance=producto)

    return render(request, 'Proteccion/editar_Producto_Proteccion.html', {
        'form': form
    })

def editar_producto_almacen(request, producto_id):
    producto = get_object_or_404(Producto_almacen, pk=producto_id)

    if request.method == 'POST':
        form = FormsProducto_almacen(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos_Almacen')  
    else:
        form = FormsProducto_almacen(instance=producto)

    return render(request, 'Almacen/editar_Producto_almacen.html', {
        'form': form
    })

def retirar_producto_proteccion(request, producto_id):
    producto = get_object_or_404(Producto_Proteccion, pk=producto_id)

    if request.method == 'POST':
        form = FormsRetiroProductos(request.POST)
        if form.is_valid():
            cantidad_retirada = form.cleaned_data['cantidad_retirada']
            if cantidad_retirada <= producto.cantidad_disponible:
                producto.cantidad_disponible -= cantidad_retirada
                producto.save()

                retiro = form.save(commit=False)
                retiro.producto_proteccion = producto
                retiro.save()

                return redirect('productos_Proteccion')
            else:
                form.add_error('cantidad_retirada', 'La cantidad a retirar es mayor que la disponible')
    else:
        form = FormsRetiroProductos()

    return render(request, 'Proteccion/retirar_Producto_Proteccion.html', {
        'form': form,
        'producto': producto
    })

def retirar_producto_almacen(request, producto_id):
    producto = get_object_or_404(Producto_almacen, pk=producto_id)

    if request.method == 'POST':
        form = FormsRetiroProductos(request.POST)
        if form.is_valid():
            cantidad_retirada = form.cleaned_data['cantidad_retirada']
            if cantidad_retirada <= producto.cantidad_disponible:
                producto.cantidad_disponible -= cantidad_retirada
                producto.save()

                retiro = form.save(commit=False)
                retiro.producto_almacen = producto
                retiro.save()

                return redirect('productos_Almacen')
            else:
                form.add_error('cantidad_retirada', 'La cantidad a retirar es mayor que la disponible')
    else:
        form = FormsRetiroProductos()

    return render(request, 'Almacen/retirar_Producto_Almacen.html', {
        'form': form,
        'producto': producto
    })


def retiros(request):
    retiro = RetiroProducto.objects.all()
    return render(request, 'Retiros/lista_retiros.html', {
        'retiro':retiro,
    })

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto_Proteccion, pk=producto_id)  

    if request.method == 'POST':
        producto.delete()
        return redirect('productos_Proteccion')  

    return render(request, 'Proteccion/eliminar_producto.html', {'producto': producto})

def eliminar_Producto_almacen(request, producto_id):
    producto = get_object_or_404(Producto_almacen, pk=producto_id)  

    if request.method == 'POST':
        producto.delete()
        return redirect('productos_Almacen')  

    return render(request, 'Almacen/eliminar_Producto_almacen.html', {'producto': producto})

def ejecutar_git(request):
    try:
        # Ejecutar git add .
        subprocess.run(["git", "add", "."], check=True)

        # Obtener la fecha y hora actual
        now = datetime.now()
        fecha_hora = now.strftime("%Y-%m-%d %H:%M:%S")

        # Ejecutar git commit con un mensaje que incluya la fecha y hora
        subprocess.run(["git", "commit", "-m", f"actualizacion {fecha_hora}"], check=True)

        # Ejecutar git push
        subprocess.run(["git", "push"], check=True)

        # Si todo salió bien, devolver una respuesta exitosa
        return redirect('/')
    except subprocess.CalledProcessError as e:
        # En caso de error, devolver un mensaje de error
        return HttpResponse(f"Error al ejecutar comandos de git: {e}", status=500)