import unittest
from api import app

class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_material_by_name_existing(self):
        materials = ['Hydrokenoralstonite', 'Abernathyite', 'Marcasite', 'Andalusite', 'Lawsonite']
        for material in materials:
            response = self.app.get('/material/'+material)
            data = response.json
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['name'], material)
    
    def test_get_material_by_name_nonexistent(self):
        response = self.app.get('/material/NonExistentMaterial')
        data = response.json
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Material not found')

if __name__ == '__main__':
    unittest.main()
