from django.db import connection


class Producto:

    def __init__(self, id, codigo, nombre, precio, stock):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": float(self.precio),
            "stock": self.stock,
        }


    @staticmethod
    def listar():
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, codigo, nombre, precio, stock FROM productos ORDER BY nombre")
            filas = cursor.fetchall()
        return [Producto(*fila) for fila in filas]

    @staticmethod
    def buscar_por_id(id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, codigo, nombre, precio, stock FROM productos WHERE id = %s", [id])
            fila = cursor.fetchone()
        return Producto(*fila) if fila else None

    @staticmethod
    def buscar_por_codigo(codigo):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, codigo, nombre, precio, stock FROM productos WHERE codigo = %s", [codigo])
            fila = cursor.fetchone()
        return Producto(*fila) if fila else None


    def insertar(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO productos (codigo, nombre, precio, stock) VALUES (%s, %s, %s, %s)",
                [self.codigo, self.nombre, self.precio, self.stock],
            )
            self.id = cursor.lastrowid 

    def actualizar(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE productos SET codigo = %s, nombre = %s, precio = %s, stock = %s WHERE id = %s",
                [self.codigo, self.nombre, self.precio, self.stock, self.id],
            )

    def eliminar(self):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM productos WHERE id = %s", [self.id])

    def tiene_ventas(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM detalle_venta WHERE producto_id = %s", [self.id])
            cantidad = cursor.fetchone()[0]
        return cantidad > 0
