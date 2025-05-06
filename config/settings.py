import os

class Settings:
    # SMTP Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_APP_PASSWORD = os.getenv('SMTP_APP_PASSWORD')

    # Paytm Configuration
    PAYTM_MERCHANT_KEY = os.getenv('PAYTM_MERCHANT_KEY')
    PAYTM_MID = os.getenv('PAYTM_MID')
    PAYTM_BASE_URL = "https://secure.paytmpayments.com"

settings = Settings() 