import os
from solders.keypair import Keypair

class Utils:
    
    @classmethod
    def get_local_wallet(self):
        wallet_path = os.getenv('LOCAL_WALLET_PATH')
        with open(wallet_path) as seed_file:
            file_contents = seed_file.read()
            return Keypair.from_json(file_contents)

