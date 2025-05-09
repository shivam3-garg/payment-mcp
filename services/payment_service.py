import requests
import json
from paytmchecksum import PaytmChecksum
import pprint
from typing import Optional

class PaymentService:
    def __init__(self, merchant_key: str, mid: str):
        self.merchant_key = merchant_key
        self.mid = mid
        self.base_url = "https://secure.paytmpayments.com"
    def create_payment_link(self, recipient_name: str, purpose: str, customer_email: str,
                            customer_mobile: str, amount: float) -> str:
        """Create a payment link for the specified recipient"""
        
        # ====== ✅ DEBUG LOGGING START ======
        logger.info("====== 🧩 Debug Start: create_payment_link ======")
        logger.info(f"Using MID: {self.mid}")
        logger.info(f"Using Base URL: {self.base_url}")
        logger.info(f"Recipient: {recipient_name}, Purpose: {purpose}")
        logger.info(f"Customer Email: {customer_email}, Customer Mobile: {customer_mobile}")
        logger.info(f"Amount: {amount}")
        logger.info(f"sendEmail flag: {bool(customer_email)}")
        logger.info(f"sendSms flag: {bool(customer_mobile)}")
        # ====== ✅ DEBUG LOGGING END ======

        paytmParams = {
            "body": {
                "mid": self.mid,
                "linkType": "GENERIC" if amount is None else "FIXED",
                "linkDescription": f"Payment for {purpose}",
                "linkName": f"{purpose.replace(' ', '_')}_{recipient_name.replace(' ', '_')}",
                "sendSms": bool(customer_mobile),   # ✅ FIXED LOGIC
                "sendEmail": bool(customer_email), # ✅ FIXED LOGIC
                "maxPaymentsAllowed": 1,
                "customerContact": {
                    "customerName": recipient_name,
                    "customerEmail": customer_email,
                    "customerMobile": customer_mobile
                }
            }
        }

        if amount is not None:
            paytmParams["body"]["amount"] = amount

        # Log the payload
        logger.info("Payload sent to Paytm:")
        pprint.pprint(paytmParams)

        checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), self.merchant_key)
        paytmParams["head"] = {
            "tokenType": "AES",
            "signature": checksum
        }

        try:
            response = requests.post(
                f"{self.base_url}/link/create",
                data=json.dumps(paytmParams),
                headers={"Content-type": "application/json"}
            )

            response_data = response.json()
            logger.info("Raw response from Paytm:")
            pprint.pprint(response_data)

            if response_data["body"]["resultInfo"]["resultStatus"] == "SUCCESS":
                short_url = response_data["body"]["shortUrl"]
                link_id = response_data["body"]["linkId"]
                logger.info(f"✅ Payment link created successfully. Link ID: {link_id}, Short URL: {short_url}")
                return {
                    "payment_link_id": link_id,
                    "short_url": short_url,
                    "email_sent": bool(customer_email),
                    "sms_sent": bool(customer_mobile)
                }

            logger.warning(f"❌ Failed to create payment link: {response_data['body']['resultInfo']['resultMessage']}")
            return f"Failed to create payment link: {response_data['body']['resultInfo']['resultMessage']}"

        except Exception as e:
            logger.exception("💥 Exception while creating payment link")
            return f"Error creating payment link: {str(e)}"


    def fetch_payment_links(self) -> str:
        """Fetch all payment links created by the merchant"""
        paytmParams = {
            "body": {"mid":self.mid},
        }
        checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), self.merchant_key)
        paytmParams["head"] = {
            "tokenType": "AES",
            "channelId": "WEB",
            "signature": checksum
        }
        try:
            response = requests.post(
                f"{self.base_url}/link/fetch",
                data=json.dumps(paytmParams),
                headers={"Content-type": "application/json"}
            ).json()

            if response["body"]["resultInfo"]["resultStatus"] == "SUCCESS":
                links = response["body"]["links"]
                if not links:
                    return "No payment links found."
                
                result = "Available Payment Links:\n"
                for link in links:
                    status = link.get("status", "PENDING")
                    result += (f"Link ID: {link['linkId']}, "
                              f"Name: {link['linkName']}, "
                              f"Short URL: {link['shortUrl']}, "
                              f"Status: {status}, "
                              f"Created: {link['createdDate']}, "
                              f"Expires: {link['expiryDate']}\n")
                return result
            return f"Failed to fetch payment links: {response['body']['resultInfo']['resultMessage']}"
        except Exception as e:
            return f"Error fetching payment links: {str(e)}"

    def fetch_transactions_for_link(self, link_id: str) -> str:
        """Fetch all transactions for a specific payment link"""
        paytmParams = {
            "body": {
                "mid": self.mid,
                "linkId": link_id,
                "fetchAllTxns": False
            },
            "head": {
                "tokenType": "AES",
                "signature": PaytmChecksum.generateSignature(
                    json.dumps({"mid": self.mid, "linkId": link_id, "fetchAllTxns": False}), 
                    self.merchant_key
                )
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/link/fetchTransaction",
                data=json.dumps(paytmParams),
                headers={"Content-type": "application/json"}
            ).json()

            if response["body"]["resultInfo"]["resultStatus"] == "SUCCESS":
                orders = response["body"].get("orders", [])
                if not orders:
                    return f"No transactions found for link ID {link_id}."
                
                result = f"Transactions for Link ID {link_id}:\n"
                for order in orders:
                    result += (f"Transaction ID: {order['txnId']}, "
                              f"Order ID: {order['orderId']}, "
                              f"Amount: {order['txnAmount']}, "
                              f"Status: {order['orderStatus']}, "
                              f"Completed: {order['orderCompletedTime']}, "
                              f"Customer Phone: {order.get('customerPhoneNumber', 'N/A')}, "
                              f"Customer Email: {order.get('customerEmail', 'N/A')}\n")
                return result
            return f"Failed to fetch transactions: {response['body']['resultInfo']['resultMessage']}"
        except Exception as e:
            return f"Error fetching transactions: {str(e)}" 