import requests
from config import shipstation_auth
from datetime import datetime


def mark_shipped(
    order_id,
    tracking_number,
):
    url = "https://ssapi.shipstation.com/orders/markasshipped"

    data = {
        "orderId": order_id,
        "carrierCode": "fedex",
        "shipDate": datetime.today().strftime("%Y-%m-%d"),
        "trackingNumber": tracking_number,
        "notifyCustomer": True,
        "notifySalesChannel": True,
    }
    r = requests.post(url, auth=shipstation_auth, json=data)
    print(r.text)


def get_order_id(po_number):
    url = "https://ssapi.shipstation.com/orders?orderNumber=" + po_number
    r = requests.get(url, auth=shipstation_auth)
    return r.json()["orders"][0]["orderId"]
