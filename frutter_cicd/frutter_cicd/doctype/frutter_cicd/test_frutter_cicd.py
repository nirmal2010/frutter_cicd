# Copyright (c) 2024, nirmalrajaa@frutterlabs.com and Contributors
# See license.txt

import unittest
from unittest.mock import patch
import frappe
from frutter_cicd.frutter_cicd.frutter_cicd.doctype.frutter_cicd.frutter_cicd import process_sale_log

class TestProcessSaleLog(unittest.TestCase):
    @patch('frappe.new_doc')
    @patch('frappe.get_doc')
    @patch('frappe.get_cached_doc')
    @patch('frappe.get_all')
    @patch('frappe.db.get_value')
    def test_process_sale_log(self, mock_get_value, mock_get_all, mock_get_cached_doc, mock_get_doc, mock_new_doc):
        # Mock the necessary frappe functions
        mock_new_doc.return_value = frappe.get_doc({"doctype": "Elbrit Sales Log"})
        mock_get_doc.return_value = frappe.get_doc({"doctype": "Target Working Settings"})
        mock_get_cached_doc.return_value = frappe.get_doc({"doctype": "Distributor"})
        mock_get_all.return_value = [{"name": "test"}]
        mock_get_value.return_value = 10

        # Call the function with test data
        process_sale_log('test_name', 'test_customer', 'test_dist', '2022-01-01', '12:00', '0', 'test_item_code', 'test_item_name', 'test_pack', 10, 'test_uom', 100, 10, 10, 'test_batch_no', '2023-01-01', 10)

        # Assert that the new_doc function was called with the correct argument
        mock_new_doc.assert_called_with("Elbrit Sales Log")

        # Add more assertions here based on what you expect the function to do

if __name__ == '__main__':
    unittest.main()

		# Assert that the title of the retrieved document matches the original title
		self.assertEqual(retrieved_frutter_cicd.title, "Test Document")
