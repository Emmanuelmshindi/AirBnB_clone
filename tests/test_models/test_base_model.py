import unittest

from unittest.mock import patch

from datetime import datetime

from models.base_model import BaseModel

from model.engine.filestorage import new, save

class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.model = BaseModel()

    def test_id_is_string(self):
        self.assertIsInstance(self.model.id, str)

    def test_created_at_is_datetime(self):
        self.assertIsInstance(self.model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_save_updates_updated_at(self):
        old_updated_at = self.model.updated_at
        self.model.save()
        new_updated_at = self.model.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)

    def test_to_dict_contains_class_name(self):
        model_dict = self.model.to_dict()
        self.assertIn('class', model_dict)
        self.assertEqual(model_dict['class'], 'BaseModel')

    def test_to_dict_contains_created_at(self):
        model_dict = self.model.to_dict()
        self.assertIn('created_at', model_dict)
        self.assertIsInstance(model_dict['created_at'], str)

    def test_to_dict_contains_updated_at(self):
        model_dict = self.model.to_dict()
        self.assertIn('updated_at', model_dict)
        self.assertIsInstance(model_dict['updated_at'], str)

    def test_to_dict_contains_instance_attributes(self):
        self.model.name = "My model"
        self.model.my_number = 89
        model_dict = self.model.to_dict()
        self.assertIn('name', model_dict)
        self.assertIn('my_number', model_dict)
        self.assertEqual(model_dict['name'], "My model")
        self.assertEqual(model_dict['my_number'], 89)

    def test_kwargs_attributes(self):
        # Create an instance of BaseModel with kwargs
        kwargs = {
            'name' = 'Test Model',
            'value' = 42
        }
        model = BaseModel(**kwargs)
        self.assertEqual(model.name, 'Test Model')
        self.assertEqual(model.value, 42)

    def test_kwargs_exclusion(self):
        # Exclude the class key
        kwargs = {
            'name' = 'Test Model',
            'value' = 42,
            '__class__' = 'Invalid'
        }
        model = BaseModel(**kwargs)
        self.assertFalse(hasAttr('__class__', model))

    def test_to_dict_conversion(self):
        # Create an instance of BaseModel with kwargs
        kwargs = {
            'name' = 'Test Model'
            'value' = 42,
        }
        model = BaseModel(**kwargs)
        # Convert the model to a dictionary
        model.to_dict()

        # Verify that the dictionary contains expected keys and values
        self.assertEqual(model['name'], 'Test Model')
        self.assertEqual(model['value'], 42)
        self.assertEqual(model['__class__'], 'BaseModel')

        # Verify that created_at and updated_at are strings
        self.assertIsInstance(model['created_at'], str)
        self.assertIsInstance(model['updated_at'], str)

        # Verify that created_at and updated_at can be parsed to datetime
        created_at = datetime.fromisoformat(model_dict['created_at']
        updated_at = datetime.fromisoformat(model_dict['updated_at']
        self.assertIsInstance(created_at, datetime)
        self.assertIsInstance(updated_at, datetime)

    @patch('storage.save')
    def test_save_updates_updated_at(self, mock_save):
        old_updated_at = self.model.updated_at
        self.model.save()
        new_updated_at = self.model.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)

    @patch('storage.save')
    def test_save_calls_storage_save(self, mock_save):
        self.model.save()
        mock_save.assert_called_once()

    @patch('storage.save')
    def test_save_calls_storage_save_with_correct_arguments(self, mock_save):
        self.model.save()
        mock_save.assert_called_with()

    @patch('storage.new')
    def test_init_calls_storage_new_with_self(self, mock_new):
        self.base_model = BaseModel()
        mock_new.assert_called_once_with(self.base_model)

    @patch('storage.save')
    def test_init_calls_storage_save_if_kwargs_not_present(self, mock_save):
        self.base_model = BaseModel()
        mock_save.assert_called_once()

    @patch('storage.save')
    def test_init_does_not_call_storage_save_if_kwargs_present(self, mock_save):
        self.base_model = BaseModel(name = 'Example')
        mock_save.assert_not_called()
