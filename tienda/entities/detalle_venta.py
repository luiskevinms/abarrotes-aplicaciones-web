"""
Entidad DetalleVenta: representa una fila de la tabla 'detalle_venta'
(un articulo dentro de una venta).
"""
from django.db import connection


class DetalleVenta:

    def __init__(self, id, venta_id, producto_id, cantidad, precio_unitario, subtotal, nombre=""):
        self.id = id
        self.venta_id = venta_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal
        self.nombre = nombre  #del producto

    def to_dict(self):
        return {
            "producto_id": self.producto_id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio_unitario": float(self.precio_unitario),
            "subtotal": float(self.subtotal),
        }

    @staticmethod
    def listar_por_venta(venta_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT d.id, d.venta_id, d.producto_id, d.cantidad,
                       d.precio_unitario, d.subtotal, p.nombre
                FROM detalle_venta d
                JOIN productos p ON p.id = d.producto_id
                WHERE d.venta_id = %s
                """,
                [venta_id],
            )
            filas = cursor.fetchall()
        return [DetalleVenta(*fila) for fila in filas]

    def insertar(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [self.venta_id, self.producto_id, self.cantidad, self.precio_unitario, self.subtotal],
            )
            self.id = cursor.lastrowid
