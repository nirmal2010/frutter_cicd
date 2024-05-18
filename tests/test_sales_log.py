
import unittest
from unittest.mock import patch
import frappe
from frutter_cicd.frutter_cicd.custom.sales_log import process_sale_log

class TestProcessSaleLog(unittest.TestCase):
    @patch('frappe.new_doc')
    @patch('frappe.get_doc')
    def test_process_sale_log(self, mock_get_doc, mock_new_doc):
        # Mock the Elbrit Sales Log document
        mock_el_log = frappe.get_doc({
            'doctype': 'Elbrit Sales Log',
            'fsl_name': '',
            'fsl_distributor': '',
            'fsl_customer': '',
            # ... add all other fields here ...
        })
        mock_new_doc.return_value = mock_el_log

        # Mock the Target Working Settings document
        mock_target_working_settings = frappe.get_doc({
            'doctype': 'Target Working Settings',
            'free_item_scheme': 1.0,
            'sample': 1.0,
            'claim_offer_reimbrusement': 1.0,
            # ... add all other fields here ...
        })
        mock_get_doc.return_value = mock_target_working_settings

        # Call the function with some test data
        process_sale_log('name', 'customer', 'fsl_dist', 'posting_date', 'posting_time', 'is_return', 'item_code', 'item_name', 'fsl_pack', 'qty', 'uom', 'amount', 'fsl_ptr', 'rate', 'batch_no', 'fsl_exp_date', 'fsl_pts', 'is_free', 'fsl_reason', 'return_against', 'fsl_credit_note', 'reason_for_issuing_document', 'claim_id', 'sample_id')

        # Check that the document fields were updated correctly
        self.assertEqual(mock_el_log.fsl_name, 'name')
        self.assertEqual(mock_el_log.fsl_distributor, 'fsl_dist')
        self.assertEqual(mock_el_log.fsl_customer, 'customer')
        # ... add assertions for all other fields here ...

if __name__ == '__main__':
    unittest.main()


# import unittest

# def sum_of_two_numbers(a, b):
#     return a + b

# class TestSum(unittest.TestCase):
#     def test_sum_of_two_numbers(self):
#         # Arrange
#         a = 7
#         b = 7

#         # Act
#         result = sum_of_two_numbers(a, b)

#         # Assert
#         self.assertEqual(result, 14)

# if __name__ == '__main__':
#     unittest.main()
