# import unittest
# from unittest.mock import patch
# import frappe
# # from frutter_cicd.frutter_cicd.custom import sales_log

# class TestSalesLog(unittest.TestCase):
#     @patch('frappe.new_doc')
#     @patch('frappe.get_doc')
#     @patch('frappe.db.get_value')
#     @patch('frappe.get_cached_doc')
#     @patch('frappe.get_all')
#     def test_process_sale_log(self, mock_get_all, mock_get_cached_doc, mock_get_value, mock_get_doc, mock_new_doc):
#         # Arrange
#         mock_new_doc.return_value = frappe._dict()
#         mock_get_doc.return_value = frappe._dict()
#         mock_get_value.return_value = 1
#         mock_get_cached_doc.return_value = frappe._dict()
#         mock_get_all.return_value = [frappe._dict(name='test')]

#         # Act
#         sales_log.process_sale_log('name', 'customer', 'fsl_dist', 'posting_date', 'posting_time', 'is_return', 'item_code', 'item_name', 'fsl_pack', 'qty', 'uom', 'amount', 'fsl_ptr', 'rate', 'batch_no', 'fsl_exp_date','fsl_pts', 'is_free', 'fsl_reason', 'return_against', 'fsl_credit_note', 'reason_for_issuing_document', 'claim_id', 'sample_id')

#         # Assert
#         mock_new_doc.assert_called_once_with("Elbrit Sales Log")
#         mock_get_doc.assert_called_once_with("Target Working Settings")

# if __name__ == '__main__':
#     unittest.main()


import unittest

def sum_of_two_numbers(a, b):
    return a + b

class TestSum(unittest.TestCase):
    def test_sum_of_two_numbers(self):
        # Arrange
        a = 7
        b = 7

        # Act
        result = sum_of_two_numbers(a, b)

        # Assert
        self.assertEqual(result, 14)

if __name__ == '__main__':
    unittest.main()