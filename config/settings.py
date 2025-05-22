import os

class Settings:
    def __init__(self):
        
        # Paytm Configuration
        self.PAYTM_KEY_SECRET = os.environ.get('PAYTM_KEY_SECRET')
        self.PAYTM_MID = os.environ.get('PAYTM_MID')
        self.PAYTM_BASE_URL = "https://secure.paytmpayments.com"

settings = Settings() 