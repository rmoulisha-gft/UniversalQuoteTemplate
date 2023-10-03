import requests
import base64
import json
import os

token = os.environ.get("fmDashtoken")
# 230726-0289

def checkout(work_order_id):
    url = f"https://fmdashboard-staging.herokuapp.com/api/work_orders/{work_order_id}/checkout"
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "checkout": {
            "description": "This is the description of my checkout. Thanks!",
            "status": "150",
            "resolution": "Repaired"
        }
    }
    payload_json = json.dumps(payload)
    response = requests.post(url, headers=headers, data=payload_json)

def getNeedToQuote():
    url = f"https://fmdashboard-staging.herokuapp.com/api/work_orders/status_filter=150&?token={token}"
    headers = {
        'Authorization': f'Bearer :{token}',
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        work_orders = response.json()
        print(work_orders)
    else:
        print(f"Request failed with status code: {response.status_code}")

def submitFmQuotes(pdf_base64, work_order_id, incurred, proposed, labor_df, trip_df, parts_df, misc_df, materials_df, sub_df, total, taxTotal):
    url = f"https://fmdashboard-staging.herokuapp.com/api/work_orders/{work_order_id}/checkout"
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "checkout": {
            "description": "This is the description of my checkout. Thanks!",
            "status": "150",
            "resolution": "Repaired"
        }
    }
    payload_json = json.dumps(payload)
    response = requests.post(url, headers=headers, data=payload_json)
    
    api_url = f"https://fmdashboard-staging.herokuapp.com/api/work_orders/{work_order_id}/quotes?token={token}"

    # with open("input.pdf", "rb") as pdf_file:
    #     pdf_content = pdf_file.read()
    #     pdf_base64 = base64.b64encode(pdf_content).decode("utf-8")

    laborIncurredmask = (labor_df["Incurred/Proposed"] == "Incurred")
    laborProposedmask = (labor_df["Incurred/Proposed"] == "Proposed")
    tripIncurredmask = (trip_df["Incurred/Proposed"] == "Incurred")
    tripProposedmask = (trip_df["Incurred/Proposed"] == "Proposed")
    partsIncurredmask = (parts_df["Incurred/Proposed"] == "Incurred")
    partsProposedmask = (parts_df["Incurred/Proposed"] == "Proposed")

    payload = {
        "quote": {
        "id": work_order_id,
        "incurred_description": incurred,
        "proposed_description": proposed,
        "ready": True,
        "incurred_trip_charge": trip_df.loc[tripIncurredmask,'EXTENDED'].sum(), 
        "proposed_trip_charge": trip_df.loc[tripProposedmask,'EXTENDED'].sum(), 
        "total": total,
        "make": "string",
        "model": "string",
        "serial_number": "string",
        "simple_quote": True,
        "document": pdf_base64,
        "document_cache": "string",
        "incurred_time" : labor_df.loc[laborIncurredmask,'EXTENDED'].sum(),
        "proposed_time" : labor_df.loc[laborProposedmask,'EXTENDED'].sum(),
        "incurred_material": parts_df.loc[partsIncurredmask,'EXTENDED'].sum(),
        "proposed_material": parts_df.loc[partsProposedmask,'EXTENDED'].sum() + misc_df['EXTENDED'].sum() + materials_df['EXTENDED'].sum() + sub_df['EXTENDED'].sum(),
        "tax_total": taxTotal,
        "approval_document_file": "string"
    }
    }
    headers = {}
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        # data = response.json()
        # print(data)
        print("Quote submitted. Quote ID:", response.text)
    else:
        print("Failed to submit quote. Status code:", response.status_code)
