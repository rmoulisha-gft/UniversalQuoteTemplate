import requests
import base64
import json
import os

token = os.environ.get("fmDashtoken")
# 230726-0289

def submitFmQuotes(pdf_base64, work_order_id, incurred, proposed, labor_df, trip_df, parts_df, misc_df, materials_df, sub_df, total, taxTotal):
    # work_order_id = "118918"
    api_url = f"https://fmdashboard-staging.herokuapp.com/api/work_orders/{work_order_id}/quotes?token={token}"

    with open("input.pdf", "rb") as pdf_file:
        pdf_content = pdf_file.read()
        pdf_base64 = base64.b64encode(pdf_content).decode("utf-8")

    quote_data = {
        "id": work_order_id,
        "incurred_description": incurred,
        "proposed_description": proposed,
        "ready": True,
        "incurred_trip_charge": labor_df['Incurred'].sum() + trip_df['Incurred'].sum(), 
        "proposed_trip_charge": labor_df['Proposed'].sum() + trip_df['Proposed'].sum(), 
        "total": f"{total:.2f}",
        "make": "string",
        "model": "string",
        "serial_number": "string",
        "simple_quote": True,
        "document": pdf_base64,
        "document_cache": "string",
        "incurred_time": 0,
        "incurred_material": parts_df['Incurred'].sum(),
        # incurred parts
        "proposed_time": 0,
        "proposed_material": parts_df['Incurred'].sum() + misc_df.sum() + materials_df.sum() + sub_df.sums(),
        # proposed parts + misc + material + sub
        "tax_total": f"{taxTotal:.2f}",
        "approval_document_file": "string"
    }

    response = requests.post(api_url, json=quote_data)

    if response.status_code == 200:
        data = response.json()
        print("Quote submitted successfully. Quote ID:", data.get("id"))
    else:
        print("Failed to submit quote. Status code:", response.status_code)

# getOpenWO("getWO1.json")
# submitQuotes()
# getOpenWO("getWO2.json")
