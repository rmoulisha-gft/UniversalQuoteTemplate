import requests
import base64
import json
import os

token = "6d05c4b7-0078-4129-a925-86d609a3cfef"
token = os.environ.get("fmDashtoken")

def getOpenWO(filename):
    api_url = f"https://fmdashboard-staging.herokuapp.com/api/work_orders?token={token}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        # Save the data to a JSON file
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)

        print("Work orders saved to getWO.json")

    else:
        print("Failed to fetch work orders. Status code:", response.status_code)

def submitFmQuotes(pdf_base64):
    work_order_id = "118918"
    api_url = f"https://fmdashboard-staging.herokuapp.com/api/work_orders/{work_order_id}/quotes?token={token}"

    # with open("input.pdf", "rb") as pdf_file:
    #     pdf_content = pdf_file.read()
    #     pdf_base64 = base64.b64encode(pdf_content).decode("utf-8")

    quote_data = {
        "id": work_order_id,
        "incurred_description": "This is the incurred description of my first test ",
        "proposed_description": "This is the proposed_description of my first test",
        "ready": True,
        "incurred_trip_charge": 0,
        "proposed_trip_charge": 0,
        "total": 0,
        "make": "string",
        "model": "string",
        "serial_number": "string",
        "simple_quote": True,
        "document": pdf_base64,
        "document_cache": "string",
        "incurred_time": 0,
        "incurred_material": 0,
        "proposed_time": 0,
        "proposed_material": 0,
        "tax_total": 0,
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