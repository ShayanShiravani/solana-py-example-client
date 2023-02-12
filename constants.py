import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = {
    "mainnet": "https://rpc.ankr.com/solana",
    "testnet": "https://api.testnet.solana.com",
    "devnet": "https://rpc.ankr.com/solana_devnet",
    "localhost": "http://localhost:8899"
}

SECRET_KEY = os.getenv("SECRET_KEY")
