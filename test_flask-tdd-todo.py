import unittest
import os
import json
from app import create_app, db


class TodoAPPTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'buy pinneapples for hell pizza.'}

        with self.app.app_context():
            db.create_all()

    def test_bucketlist_creation(self):
        """Test API can create"""
        res = self.client().post('/todolist/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('buy pinneapples', str(res.data))

    def test_api_can_get_all_todolist(self):
        """Test API can get a list of todos."""
        res = self.client().post('/todolist/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/todolist/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('buy pinneapples', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get an item by it's id."""
        rv = self.client().post('/todolist/', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/todolist/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('buy pinneapples', str(result.data))


    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing item"""
        rv = self.client().post(
            '/todolist/',
            data={'name': 'Get tickets.'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/todolist/1',
            data={
                "name": "Get tickets and apples."
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/todolist/1')
        self.assertIn('apples', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete"""
        rv = self.client().post(
            '/todolist/',
            data={'name': 'a thing to delete'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/todolist/1')
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/todolist/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()

