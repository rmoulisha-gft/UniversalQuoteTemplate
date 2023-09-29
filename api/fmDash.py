import requests
import base64
import json
import os

token = os.environ.get("fmDashtoken")
# 230726-0289

def submitFmQuotes(pdf_base64, work_order_id, incurred, proposed, labor_df, trip_df, parts_df, misc_df, materials_df, sub_df, total, taxTotal):
    api_url = f"https://fmdashboard-staging.herokuapp.com/api/work_orders/{work_order_id}/quotes?token={token}"

    with open("input.pdf", "rb") as pdf_file:
        pdf_content = pdf_file.read()
        pdf_base64 = base64.b64encode(pdf_content).decode("utf-8")
    
    laborIncurredmask = (labor_df["Incurred/Proposed"] == "Incurred")
    laborProposedmask = (labor_df["Incurred/Proposed"] == "Proposed")
    tripIncurredmask = (trip_df["Incurred/Proposed"] == "Incurred")
    tripProposedmask = (trip_df["Incurred/Proposed"] == "Proposed")
    partsIncurredmask = (parts_df["Incurred/Proposed"] == "Incurred")
    partsProposedmask = (parts_df["Incurred/Proposed"] == "Proposed")


    quote_data = {
        "id": work_order_id,
        "incurred_description": incurred,
        "proposed_description": proposed,
        "ready": True,
        "incurred_trip_charge": labor_df.loc[laborIncurredmask,'EXTENDED'].sum() + trip_df.loc[tripIncurredmask,'EXTENDED'].sum(), 
        "proposed_trip_charge": labor_df.loc[laborProposedmask,'EXTENDED'].sum() + trip_df.loc[tripProposedmask,'EXTENDED'].sum(), 
        "total": total,
        "make": "string",
        "model": "string",
        "serial_number": "string",
        "simple_quote": True,
        "document": "",
        "document_cache": "string",
        "incurred_time": 0,
        "incurred_material": parts_df.loc[partsIncurredmask,'EXTENDED'].sum(),
        # incurred parts
        "proposed_time": 0,
        "proposed_material": parts_df.loc[partsProposedmask,'EXTENDED'].sum() + misc_df['EXTENDED'].sum() + materials_df['EXTENDED'].sum() + sub_df['EXTENDED'].sum(),
        # proposed parts + misc + material + sub
        "tax_total": taxTotal,
        "approval_document_file": "string"
    }
    print(quote_data)

    response = requests.post(api_url, json=quote_data)

    if response.status_code == 200:
        data = response.json()
        print("Quote submitted successfully. Quote ID:", data.get("id"))
    else:
        print("Failed to submit quote. Status code:", response.status_code)
