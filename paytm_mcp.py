import sys
import os
import logging
from typing import Optional, List

from mcp.server.fastmcp import FastMCP
from services.payment_service import PaymentService
from config.settings import settings
from utils.models import PaymentLink, Transaction

# Load environment variables (if running locally)
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("paytm-mcp-server")

# Initialize services
try:
    mid = os.environ.get("PAYTM_MID")
    key = os.environ.get("PAYTM_KEY_SECRET")

    if not mid or not key:
        logger.error("Missing PAYTM credentials. Please set PAYTM_MID and PAYTM_KEY_SECRET.")
        sys.exit(1)

    payment_service = PaymentService(key, mid)
except Exception as e:
    logger.error(f"Failed to initialize services: {str(e)}")
    sys.exit(1)


@mcp.tool()
def create_payment_link(
    recipient_name: str,
    purpose: str,
    customer_email: str = None,
    customer_mobile: str = None,
    amount: str = None,
) -> str:
    """
    Create a new payment link with recipient and purpose. Optional amount can be fixed.
    Either customer_email or customer_mobile must be provided.
    """
    try:
        if not customer_email and not customer_mobile:
            return "Please provide at least one of customer_email or customer_mobile."

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


@mcp.tool()
def fetch_payment_links() -> List[dict]:
    """
    Fetch all payment links created by the merchant.
    """
    try:
        links: List[PaymentLink] = payment_service.fetch_payment_links()
        if not links:
            return [{"message": "No payment links found."}]
        return [link.dict() for link in links]
    except Exception as e:
        logger.error(f"Failed to fetch payment links: {str(e)}")
        return [{"error": str(e)}]


@mcp.tool()
def fetch_transactions_for_link(link_id: str) -> List[dict]:
    """
    Fetch all transactions related to a specific payment link.
    """
    try:
        transactions: List[Transaction] = payment_service.fetch_transactions_for_link(link_id)
        if not transactions:
            return [{"message": f"No transactions found for link ID {link_id}."}]
        return [txn.dict() for txn in transactions]
    except Exception as e:
        logger.error(f"Failed to fetch transactions: {str(e)}")
        return [{"error": str(e)}]


if __name__ == "__main__":
    logger.info("Starting Paytm MCP Server...")
    mcp.run()

