"""test"""
from django.test import TestCase, Client

# Create your tests here.
class MainTest(TestCase):
    """Main Test"""
    def setUp(self):
        pass
    
    def test_index_page(self):
        client = Client()
        response = client.post("/api/index")
        self.assertEqual(response.content, b"Hello world")
