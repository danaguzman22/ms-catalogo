import requests
import logging
from app import db  # Asegúrate de importar db
from app.models.catalogo import Producto  # Asegúrate de importar el modelo correcto


class CatalogoService:
    INVENTARIO_URL = "http://localhost:5002/stock"  # Cambia el puerto según corresponda

    @staticmethod
    def obtener_producto(producto_id):
        # Obtener el producto del catálogo
        producto = Producto.obtener_producto_por_id(producto_id)

        if producto is None:
            logging.error(f"Producto con ID {producto_id} no encontrado.")
            return None  # Manejar el caso en que no se encuentra el producto

        # Consultar el inventario para la disponibilidad
        try:
            response = requests.get(f"{CatalogoService.INVENTARIO_URL}/{producto_id}")
            if response.status_code == 200:
                stock_info = response.json()
                producto.stock = stock_info.get('cantidad', 0)  # Agregar la cantidad al producto
            else:
                logging.error(f"Error al consultar inventario para el producto ID {producto_id}: {response.status_code}")
                producto.stock = 0  # Si hay un error, se puede considerar que no hay stock disponible
        except requests.exceptions.RequestException as e:
            logging.error(f"Error al conectar con el microservicio de inventario: {str(e)}")
            producto.stock = 0  # Asumir que no hay stock si no se puede conectar

        return producto

    @staticmethod
    def agregar_producto(nombre, precio, activado=True):
        nuevo_producto = Producto(nombre=nombre, precio=precio, activado=activado)
        db.session.add(nuevo_producto)
        db.session.commit()
        return nuevo_producto

    @staticmethod
    def obtener_todos_los_productos():
        return Producto.query.all()

    @staticmethod
    def activar_producto(producto_id):
        producto = Producto.obtener_producto_por_id(producto_id)
        if producto:
            producto.activado = True
            db.session.commit()
            return producto
        return None

    @staticmethod
    def desactivar_producto(producto_id):
        producto = Producto.obtener_producto_por_id(producto_id)
        if producto:
            producto.activado = False
            db.session.commit()
            return producto
        return None
    