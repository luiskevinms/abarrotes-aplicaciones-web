"""
Entidad Venta: representa una fila de la tabla 'ventas' (una compra).
"""
from datetime import datetime

from django.db import connection

from .detalle_venta import DetalleVenta


class Venta:

    def __init__(self, id, fecha, total):
        self.id = id
        self.fecha = fecha
        self.total = total
        self.detalles = []  # lista de DetalleVenta

    def to_dict(self, con_detalles=False):
        datos = {
            "id": self.id,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "total": float(self.total),
        }
        if con_detalles:
            datos["detalles"] = [d.to_dict() for d in self.detalles]
        return datos

    @staticmethod
    def listar():
        """Historial de ventas, la mas reciente primero."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, fecha, total FROM ventas ORDER BY id DESC")
            filas = cursor.fetchall()
        return [Venta(*fila) for fila in filas]

    @staticmethod
    def buscar_por_id(id):
        """Una venta con todos sus articulos."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, fecha, total FROM ventas WHERE id = %s", [id])
            fila = cursor.fetchone()
        if not fila:
            return None
        venta = Venta(*fila)
        venta.detalles = DetalleVenta.listar_por_venta(venta.id)
        return venta

    def insertar(self):
        self.fecha = datetime.now().replace(microsecond=0)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO ventas (fecha, total) VALUES (%s, %s)",
                [self.fecha, self.total],
            )
            self.id = cursor.lastrowid
