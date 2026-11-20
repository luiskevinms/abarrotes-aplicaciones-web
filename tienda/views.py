import json

from django.db import transaction
from django.http import JsonResponse

from .entities import Producto, Venta, DetalleVenta


def error(mensaje, status=400):
    return JsonResponse({"error": mensaje}, status=status)


# GET /api/productos/
def productos(request):
    if request.method == "GET":
        lista = [p.to_dict() for p in Producto.listar()]
        return JsonResponse(lista, safe=False)  # safe=False para que pueda regresar una lista

    # POST /api/productos/ para agregar productos
    if request.method == "POST":
        datos = json.loads(request.body)

        if Producto.buscar_por_codigo(datos["codigo"]):
            return error("Ya existe un producto con ese codigo")

        p = Producto(
            id=None,
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            precio=datos["precio"],
            stock=datos.get("stock", 0),
        )
        p.insertar()
        return JsonResponse(p.to_dict(), status=201)

    return error("Metodo no permitido", 405)


def producto(request, id):
    p = Producto.buscar_por_id(id)
    if p is None:
        return error("Producto no encontrado", 404)

    # GET /api/productos/5/
    if request.method == "GET":
        return JsonResponse(p.to_dict())

    # PUT /api/productos/5/ actualizar
    if request.method == "PUT":
        datos = json.loads(request.body)
        p.codigo = datos.get("codigo", p.codigo)
        p.nombre = datos.get("nombre", p.nombre)
        p.precio = datos.get("precio", p.precio)
        p.stock = datos.get("stock", p.stock)
        p.actualizar()
        return JsonResponse(p.to_dict())

    # DELETE /api/productos/5/
    if request.method == "DELETE":
        if p.tiene_ventas():
            return error("No se puede borrar: el producto ya aparece en ventas")
        p.eliminar()
        return JsonResponse({"mensaje": "Producto eliminado"})

    return error("Metodo no permitido", 405)


def producto_por_codigo(request, codigo):
    p = Producto.buscar_por_codigo(codigo)
    if p is None:
        return error("Producto no encontrado", 404)
    return JsonResponse(p.to_dict())


def ventas(request):
    # GET /api/ventas/
    if request.method == "GET":
        lista = [v.to_dict() for v in Venta.listar()]
        return JsonResponse(lista, safe=False)

    # POST /api/ventas/  registra una compra
    if request.method == "POST":
        datos = json.loads(request.body)
        articulos = datos.get("articulos", [])

        if not articulos:
            return error("La venta no tiene articulos")

        # revisar que todo exista y haya stock suficiente y calcular el total
        total = 0
        renglones = []  # guardamos (producto, cantidad) para usarlos despues
        for a in articulos:
            p = Producto.buscar_por_id(a["producto_id"])
            if p is None:
                return error(f"No existe el producto con id {a['producto_id']}")

            cantidad = int(a["cantidad"])
            if cantidad <= 0:
                return error(f"Cantidad invalida para {p.nombre}")
            if cantidad > p.stock:
                return error(f"No hay suficiente stock de {p.nombre} (quedan {p.stock})")

            total += p.precio * cantidad
            renglones.append((p, cantidad))

        # Guardar la venta, sus detalles y descontar el stock
        # transaction.atomic() es por si algo falla no se guarda nada
        with transaction.atomic():
            venta = Venta(id=None, fecha=None, total=total)
            venta.insertar()

            for p, cantidad in renglones:
                detalle = DetalleVenta(
                    id=None,
                    venta_id=venta.id,
                    producto_id=p.id,
                    cantidad=cantidad,
                    precio_unitario=p.precio,
                    subtotal=p.precio * cantidad,
                    nombre=p.nombre,
                )
                detalle.insertar()
                venta.detalles.append(detalle)

                p.stock -= cantidad
                p.actualizar()

        return JsonResponse(venta.to_dict(con_detalles=True), status=201)

    return error("Metodo no permitido", 405)


def venta(request, id):
    # GET /api/ventas/5/
    v = Venta.buscar_por_id(id)
    if v is None:
        return error("Venta no encontrada", 404)
    return JsonResponse(v.to_dict(con_detalles=True))
