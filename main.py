import os
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana_client import SolanaClient
from constants import RPC_URL


def main():
    secret_key = os.getenv("SECRET_KEY")
    signer = Keypair.from_base58_string(secret_key)
    rpc_client = Client(RPC_URL)
    client = SolanaClient(rpc_client, signer)

    # client.transfer_lamports(
    #     signer.pubkey(), Pubkey.from_string("38FScr6QrGFJEtPmdSrqWXS8yKZvhiQeziUbnD3DYuDF"), 10000)
    receivers = [
        Pubkey.from_string("38FScr6QrGFJEtPmdSrqWXS8yKZvhiQeziUbnD3DYuDF"),
        Pubkey.from_string("9rBsDbS3C1aLxG6AqUZvSrcmHEEQDrVzCC7K8ey7QdT5")
    ]
    client.transfer_many_lamports(
        signer.pubkey(), [(rec, 1000) for rec in receivers])


load_dotenv()
main()
