import sys
import os
import logging
from typing import Optional, List
from dotenv import load_dotenv  # ✅ To load local env during development
from mcp.server.fastmcp import FastMCP
from services.payment_service import PaymentService
from config.settings import settings
from utils.models import PaymentLink, Transaction


# ✅ Load .env variables (for local dev)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("paytm-mcp-server")

# Initialize services
try:
    # email_service = EmailService()
    payment_service = PaymentService(os.environ.get("PAYTM_KEY_SECRET"),os.environ.get("PAYTM_MID"))
    logger.info("✅ PaymentService initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize services: {str(e)}")
    sys.exit(1)

# Tool: Create Payment Link
@mcp.tool()
def create_payment_link(
    recipient_name: str,
    purpose: str,
    customer_email: str = None,
    customer_mobile: str = None,
    amount: str = None,
) -> str:
    """
    Create a new payment link for receiving payments.

    This operation generates a unique payment link that can be shared with customers
    for accepting payments. The link can be customized with recipient details,
    purpose, customer details and amount.

    Required Parameters:
        recipient_name (str): Name of the person or entity receiving the payment
        purpose (str): Description or reason for the payment
        customer_email (str): Email address of the customer
        customer_mobile (str): Mobile number of the customer
        Either customer_email or customer_mobile must be provided if else please ask from the user

    Optional Parameters:
        amount (float): Fixed amount for the payment

    Note:
        - Amount can be left optional for customer to decide
        - Generated link will be valid according to system's expiry settings
        - Please ask all the required fields from the user don't assume any fields
    
    IMPORTANT NOTE:
        - if user is not providing customer_email or customer_mobile, please ask for the same don't call any tool before asking for the same
        """
    
    try:
        return payment_service.create_payment_link(
            recipient_name=recipient_name,
            purpose=purpose,
            customer_email=customer_email,
            customer_mobile=customer_mobile,
            amount=amount
        )
    except Exception as e:
        logger.error(f"Failed to create payment link: {str(e)}")
        return str(e)

# Tool: Fetch All Payment Links
@mcp.tool()
def fetch_payment_links() -> str:
    """
    Retrieve all payment links created by the merchant.

    This operation returns a comprehensive list of all payment links created,
    including both active and expired links. Each link entry contains details
    such as:
        - Link ID
        - Link Name
        - Short URL
        - Status
        - Creation Date
        - Expiry Date

    Returns:
        List[PaymentLink]: A list of PaymentLink objects containing link details
        str: Error message in case of failure
    """
    try:
        links: List[PaymentLink] = payment_service.fetch_payment_links()
        if not links:
            return "No payment links found."
        
        # result = "Available Payment Links:\n"
        # for link in links:
        #     result += (f"Link ID: {link.link_id}, "
        #               f"Name: {link.link_name}, "
        #               f"Short URL: {link.short_url}, "
        #               f"Status: {link.status}, "
        #               f"Created: {link.created_date}, "
        #               f"Expires: {link.expiry_date}\n")
        return links
    except Exception as e:
        logger.error(f"Failed to fetch payment links: {str(e)}")
        return str(e)

# Tool: Fetch Transactions for a Specific Link
@mcp.tool()
def fetch_transactions_for_link(link_id: str) -> str:
    """
    Retrieve all transactions associated with a specific payment link.

    This operation provides detailed transaction history for a given payment link,
    including successful and failed transactions.

    Parameters:
        link_id (str): Unique identifier of the payment link

    Returns:
        List[Transaction]: List of transactions containing details such as:
            - Transaction ID
            - Order ID
            - Amount
            - Status
            - Completion Time
            - Customer Contact Information
        str: Error message in case of failure
    """
    try:
        transactions: List[Transaction] = payment_service.fetch_transactions_for_link(link_id)
        if not transactions:
            return f"No transactions found for link ID {link_id}."
        
        # result = f"Transactions for Link ID {link_id}:\n"
        # for txn in transactions:
        #     result += (f"Transaction ID: {txn.txn_id}, "
        #               f"Order ID: {txn.order_id}, "
        #               f"Amount: {txn.amount}, "
        #               f"Status: {txn.status}, "
        #               f"Completed: {txn.completed_time}, "
        #               f"Customer Phone: {txn.customer_phone or 'N/A'}, "
        #               f"Customer Email: {txn.customer_email or 'N/A'}\n")
        return transactions
    except Exception as e:
        logger.error(f"Failed to fetch transactions: {str(e)}")
        return str(e)

# ✅ Final tool registration check
logger.info("✅ FastMCP initialized (tool listing not supported in v1.7.1)")
print("📦 Registered tools:")
for t in mcp._tools:
    print("🔧", t.name)