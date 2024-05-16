# Copyright (c) 2024, nirmalrajaa@frutterlabs.com and Contributors
# See license.txt

# import frappe
from frappe.tests.utils import FrappeTestCase
from frutter_cicd.doctype.frutter_cicd.frutter_cicd import FrutterCICD


class TestFrutterCICD(FrappeTestCase):

	def test_frutter_cicd_document_creation(self):
		# Create a new FrutterCICD document
		frutter_cicd = FrutterCICD()
		frutter_cicd.title = "Test Document"
		frutter_cicd.save()

		# Retrieve the document from the database
		retrieved_frutter_cicd = FrutterCICD.get(frutter_cicd.name)

		# Assert that the retrieved document is not None
		self.assertIsNotNone(retrieved_frutter_cicd)

		# Assert that the title of the retrieved document matches the original title
		self.assertEqual(retrieved_frutter_cicd.title, "Test Document")