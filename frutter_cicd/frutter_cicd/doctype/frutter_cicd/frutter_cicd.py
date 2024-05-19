# Copyright (c) 2024, nirmalrajaa@frutterlabs.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FrutterCICD(Document):
	pass


import frappe

@frappe.whitelist()
def process_sale_log(name, customer, fsl_dist, posting_date, posting_time, is_return, item_code, item_name, fsl_pack, qty, uom, amount, fsl_ptr, rate, batch_no, fsl_exp_date,fsl_pts, is_free=None, fsl_reason=None, return_against=None, fsl_credit_note=None, reason_for_issuing_document=None, claim_id=None, sample_id=None):
    # Create a new Elbrit Sales Log document
    el_log = frappe.new_doc("Elbrit Sales Log")
    #updating the values in the new document for each field
    el_log.update({
        'fsl_name': name,
        'fsl_distributor': fsl_dist,
        'fsl_customer': customer,
        'date': posting_date,
        'fsl_time': posting_time,
        'fsl_code': item_code,
        'fsl_is_return': is_return,
        'is_free': is_free,
        'fsl_item_name': item_name,
        'fsl_pack': fsl_pack,
        'fsl_quantity': qty,
        'fsl_uom': uom,
        'fsl_pts': fsl_pts,
        'fsl_amount': amount,
        'fsl_ptr': fsl_ptr,
        'fsl_rate': rate,
        'fsl_batch_no': batch_no,
        'fsl_expiry_date': fsl_exp_date,
        'sample': sample_id,
        'claim_offer': claim_id
    })
    target_working_settings = frappe.get_doc("Target Working Settings")
    #checking whether the sales invoice is a return or not
    if is_free == "1" and (is_return == "" or is_return == "0" or is_return == None or is_return == 0):
        batch_pts = frappe.db.get_value("Batch", batch_no, "fsl_pts")
        if target_working_settings.free_item_scheme:
            el_log.free_itm_val = -1 * (target_working_settings.free_item_scheme)*(float(batch_pts) * float(qty))
            el_log.total_sales = -1 * (float(batch_pts) * float(qty))
            el_log.primary_sales = -1 * (float(batch_pts) * float(qty))      
        else:
            el_log.free_itm_val = -1 * (float(batch_pts) * float(qty))
        
    elif sample_id and (is_return == "" or is_return == "0" or is_return == None or is_return == 0):
        if target_working_settings.sample:
            el_log.sample_value = -1 * (target_working_settings.sample)*(float(fsl_pts) * float(qty))
            el_log.total_sales = -1 * (float(fsl_pts) * float(qty))
            el_log.primary_sales = -1 * (float(fsl_pts) * float(qty))
        else:
            el_log.sample_value = -1 * (float(fsl_pts) * float(qty))
        
    elif claim_id and (is_return == "" or is_return == "0" or is_return == None or is_return == 0):
        if target_working_settings.claim_offer_reimbrusement:
            el_log.claim_value = -1 * (target_working_settings.claim_offer_reimbrusement)*(float(fsl_pts) * float(qty))
            el_log.total_sales = -1 * (float(fsl_pts) * float(qty))
            el_log.primary_sales = -1 * (float(fsl_pts) * float(qty))
        else:
            el_log.claim_value = -1 * (float(fsl_pts) * float(qty))
        
    elif is_return == "1" or is_return == 1:
        el_log.fsl_reason_for_issuing_document = reason_for_issuing_document,
        el_log.fsl_return_reason = fsl_reason
        el_log.fsl_return_against = return_against
        el_log.fsl_credit_note = fsl_credit_note
        
        #taking the Primary sales setting which is a single doctype for Primary sales calculation
        target_working_settings = frappe.get_doc("Target Working Settings")
        el_log.fsl_return_reason = fsl_reason
        # Check the fsl_return_reason field and calculate the total sales
        if fsl_reason == "Sales Return":
            if target_working_settings.for_sales_return:
                el_log.sales_return = float(float(el_log.fsl_amount) * float(target_working_settings.for_sales_return))
                el_log.total_sales = float(float(el_log.fsl_amount) * float(target_working_settings.for_sales_return))
                el_log.primary_sales = float(el_log.fsl_amount)
            else:
                el_log.sales_return = float(el_log.amount)
                
        elif fsl_reason == "Breakage":
            if target_working_settings.against_breakage:
                el_log.against_breakage = float(float(el_log.fsl_amount) * float(target_working_settings.against_breakage))
                el_log.total_sales = float(float(el_log.fsl_amount) * float(target_working_settings.against_breakage))
                el_log.primary_sales = float(el_log.fsl_amount)
            else:
                el_log.against_breakage = float(el_log.fsl_amount)
            
        elif fsl_reason == "Expired":
            if target_working_settings.against_expiry:
                el_log.against_expiry = float(float(el_log.fsl_amount) * float(target_working_settings.against_expiry))
                el_log.total_sales = float(float(el_log.fsl_amount) * float(target_working_settings.against_expiry))
                el_log.primary_sales = float(el_log.fsl_amount)
            else:
                el_log.against_expiry = float(el_log.fsl_amount)
            
        elif fsl_reason == "Rate Difference":
            if target_working_settings.rate_diff:
                el_log.rate_difference = float(float(el_log.fsl_amount) * float(target_working_settings.rate_diff))
                el_log.total_sales = float(float(el_log.fsl_amount) * float(target_working_settings.rate_diff))
                el_log.primary_sales = float(el_log.fsl_amount)
            else:
                el_log.rate_difference = float(el_log.fsl_amount)
        
        else:
            el_log.total_sales = float(amount)
            el_log.primary_sales = float(el_log.fsl_amount)    
   
    else:
        el_log.total_sales = float(amount)
        el_log.primary_sales = float(el_log.fsl_amount)

    dist_name = frappe.get_cached_doc("Distributor", fsl_dist)
    hq_doc = frappe.get_cached_doc("HQ", dist_name.fsl_cfa_hq)
    for sale_team in hq_doc.fsl_sales_team:
        sales_person = sale_team.get('fsl_sales_person')    

        # itm_sal_map = frappe.get_cached_doc("Item Sales Team Mapping", {"fsl_sales_team": sale_team})
        st_name = frappe.get_cached_doc("Elbrit Sales Team", sales_person)
        docs = frappe.get_all("Item Sales Team Mapping", filters={"fsl_sales_team": sales_person}, order_by="creation desc", limit_page_length=1)
        if docs and st_name.fsl_is_active == 1:
            itm_sal_map = frappe.get_doc("Item Sales Team Mapping", docs[0].name)
        else:
            itm_sal_map = None

        try:
            for ite in itm_sal_map.fsl_item_table:
                if item_code == ite.item_code:
                    el_log.update({
                        'fsl_sales_team': sales_person,
                        'fsl_sales_team_mapping': itm_sal_map.name,
                        # 'fsl_business_executive': e_name,
                        'fsl_hq': hq_doc.name,
                    })
                    amount = float(amount)
                    # employee = frappe.get_doc("Employee", e_name)
                    el_log.fsl_reportees = []

                    # for reportee in employee.fsl_employee_reportees:
                    #     if reportee.designation == "Area Business Manager":
                    #         rep_abm = frappe.get_value("Employee", {"employee_name": reportee.employee}, "name")
                    #         el_log.reporting_abm = rep_abm
                    #         break
        except:
            # def send_email(id,n): 
            notification = frappe.new_doc("Notification Log")
            users_ids = frappe.get_cached_doc("Target Working Settings")
            for userid in users_ids.user_table:
                notification.for_user = userid
                notification.from_user = frappe.session.user
                notification.document_type = "Sales Invoice"
                notification.document_name = "Missing Item in Item Sales Team Mapping"
                notification.subject = (f"{item_code} is missing in Item Sales Team Mapping for the Sales Team linked to {hq_doc.name}")
                notification.type = "Alert"
                notification.insert(ignore_permissions=True)
            frappe.db.commit()
                

    el_log.insert()
    frappe.db.commit()
    