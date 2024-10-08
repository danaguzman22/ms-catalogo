import unittest
from unittest.mock import patch
from app import create_app, db
from app.models.catalogo import Producto
from app.services.catalogo_service import CatalogoService

class TestCatalogoService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Crear tablas en la base de datos para las pruebas
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        cls.app_context.pop()

    @patch('requests.get')
    def test_obtener_producto_exitoso(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: {"cantidad": 10}
        
        mock_producto = Producto(id=1, nombre="Producto 1", precio=100.0, activado=True)
        with patch.object(Producto, 'obtener_producto_por_id', return_value=mock_producto):
            resultado = CatalogoService.obtener_producto(1)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, "Producto 1")
        self.assertEqual(resultado.stock, 10)

    @patch('app.models.catalogo.Producto.crear_producto')
    def test_agregar_producto(self, mock_crear_producto):
        mock_crear_producto.return_value = Producto(id=1, nombre="Nuevo Producto", precio=150.0, activado=True)
        
        resultado = CatalogoService.agregar_producto("Nuevo Producto", 150.0)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Nuevo Producto")
        self.assertEqual(resultado.precio, 150.0)

    @patch('app.models.catalogo.Producto.obtener_producto_por_id')
    def test_activar_producto(self, mock_obtener_producto):
        mock_producto = Producto(id=1, nombre="Producto 1", precio=100.0, activado=False)
        mock_obtener_producto.return_value = mock_producto

        resultado = CatalogoService.activar_producto(1)

        self.assertIsNotNone(resultado)
        self.assertTrue(resultado.activado)

    @patch('app.models.catalogo.Producto.obtener_producto_por_id')
    def test_desactivar_producto(self, mock_obtener_producto):
        mock_producto = Producto(id=1, nombre="Producto 1", precio=100.0, activado=True)
        mock_obtener_producto.return_value = mock_producto

        resultado = CatalogoService.desactivar_producto(1)

        self.assertIsNotNone(resultado)
        self.assertFalse(resultado.activado)

    @patch('requests.get')
    def test_obtener_producto_no_encontrado(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: {"cantidad": 0}

        with patch.object(Producto, 'obtener_producto_por_id', return_value=None):
            resultado = CatalogoService.obtener_producto(999)

        self.assertIsNone(resultado)

    @patch('requests.get')
    def test_obtener_producto_error_inventario(self, mock_get):
        mock_get.return_value.status_code = 500
        
        mock_producto = Producto(id=1, nombre="Producto 1", precio=100.0, activado=True)
        with patch.object(Producto, 'obtener_producto_por_id', return_value=mock_producto):
            resultado = CatalogoService.obtener_producto(1)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.stock, 0)  # Debería ser 0 en caso de error de inventario

if __name__ == "__main__":
    unittest.main()
