from app import db

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    activado = db.Column(db.Boolean, default=True)

    @staticmethod
    def crear_producto(nombre, precio):
        nuevo_producto = Producto(nombre=nombre, precio=precio)
        db.session.add(nuevo_producto)
        db.session.commit()
        return nuevo_producto

    @staticmethod
    def obtener_productos():
        return Producto.query.all()

    @staticmethod
    def obtener_producto_por_id(producto_id):
        return Producto.query.get(producto_id)

    @staticmethod
    def actualizar_producto(producto_id, nombre, precio, activado):
        producto = Producto.query.get(producto_id)
        if producto:
            producto.nombre = nombre
            producto.precio = precio
            producto.activado = activado
            db.session.commit()
            return producto
        return None

    @staticmethod
    def eliminar_producto(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return True
        return False
