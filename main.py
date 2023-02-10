import os
import traceback
import argparse
from utils import Utils
from enum import Enum
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana_client import SolanaClient
from constants import RPC_URL, PROGRAM_ID
from solders.instruction import AccountMeta
from anchor_client.instructions.increment import increment
from anchor_client.instructions.initialize import initialize
from anchor_client.accounts.counter import Counter


class Cluster(Enum):
    MAINNET = 'mainnet'
    TESTNET = 'testnet'
    DEVNET = 'devnet'
    LOCALHOST = "localhost"

    def __str__(self):
        return self.value


class Method(Enum):
    TRANSFER = 'transfer'
    TRANSFER_MANY = 'transfer_many'
    PROGRAM_CALL = 'program_call'

    def __str__(self):
        return self.value


def main(method, cluster: Cluster):
    secret_key = os.getenv("SECRET_KEY")
    if cluster == Cluster.LOCALHOST:
        signer = Utils.get_local_wallet()
    else:
        signer = Keypair.from_base58_string(secret_key)
    rpc_client = Client(RPC_URL[cluster.value])
    client = SolanaClient(rpc_client, signer)

    if method == Method.TRANSFER:
        client.transfer_lamports(signer.pubkey(), Pubkey.from_string(
            "38FScr6QrGFJEtPmdSrqWXS8yKZvhiQeziUbnD3DYuDF"), 10000)
    elif method == Method.TRANSFER_MANY:
        receivers = [
            Pubkey.from_string("38FScr6QrGFJEtPmdSrqWXS8yKZvhiQeziUbnD3DYuDF"),
            Pubkey.from_string("9rBsDbS3C1aLxG6AqUZvSrcmHEEQDrVzCC7K8ey7QdT5")
        ]
        client.transfer_many_lamports(
            signer.pubkey(), [(rec, 1000) for rec in receivers])
    elif method == Method.PROGRAM_CALL:
        counterSeed = bytes("counter", "utf8");
        counter_address, nonce = Pubkey.find_program_address([counterSeed], PROGRAM_ID)
        counter = rpc_client.get_account_info(counter_address)
        count = Counter.decode(counter.value.data).count
        print(f"Program count value before increment: {count}")
        # try:
        #     initialize_instruction = initialize({"counter": counter_address, "authority": signer.pubkey()}, PROGRAM_ID)
        #     client.call_program(initialize_instruction)
        # except:
        #     print("Program alread initialized")
        instruction = increment({"counter": counter_address, "authority": signer.pubkey()}, PROGRAM_ID)
        client.call_program(instruction)


load_dotenv()
parser = argparse.ArgumentParser()
parser.add_argument("method", type=Method,
                    choices=list(Method), help="Target method to test")
parser.add_argument(
    "cluster", type=Cluster, choices=list(Cluster), help="Target cluser")
args = parser.parse_args()
try:
    main(args.method, args.cluster)
except:
    traceback.print_exc()
