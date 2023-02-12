import traceback
import argparse
from enum import Enum
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana_client import SolanaClient
from utils import Utils
from constants import RPC_URL, SECRET_KEY
from anchor_client.program_id import PROGRAM_ID
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


class Func(Enum):
    TRANSFER = 'transfer'
    TRANSFER_MANY = 'transfer_many'
    INITIALIZE = 'initialize'
    INCREMENT = 'increment'

    def __str__(self):
        return self.value


def main(func: Func, cluster: Cluster, params):

    if cluster == Cluster.LOCALHOST:
        signer = Utils.get_local_wallet()
    else:
        signer = Keypair.from_base58_string(SECRET_KEY)

    rpc_client = Client(RPC_URL[cluster.value])
    client = SolanaClient(rpc_client, signer)
    counter_seed = bytes("counter", "utf-8")
    counter_address, nonce = Pubkey.find_program_address(
        [counter_seed], PROGRAM_ID)
    counter = rpc_client.get_account_info(counter_address)
    is_initialized = False
    if counter.value:
        is_initialized = True
    if func == Func.TRANSFER:
        client.transfer_lamports(
            signer.pubkey(), Pubkey.from_string(params['receiver']), params['amount'])
    elif func == Func.TRANSFER_MANY:
        receivers = [Pubkey.from_string(r) for r in receivers]
        client.transfer_many_lamports(
            signer.pubkey(), [(rec, params['amount']) for rec in receivers])
    elif func == Func.INITIALIZE:
        if not is_initialized:
            instruction = initialize(
                {"counter": counter_address, "authority": signer.pubkey()}
            )
            if client.call_program(instruction):
                print("The program initialized successfully")
        else:
            print("The program is already initialized")
    elif func == Func.INCREMENT:
        count = Counter.decode(counter.value.data).count
        print(f"Teh count value before incrementing: {count}")
        instruction = increment(
            {"counter": counter_address, "authority": signer.pubkey()}
        )
        client.call_program(instruction)


load_dotenv()
parser = argparse.ArgumentParser()
parser.add_argument("func", type=Func,
                    choices=list(Func), help="Desired function to test")
parser.add_argument(
    "cluster", type=Cluster, choices=list(Cluster), help="Desired cluser")
parser.add_argument(
    '-r', "--receiver",
    help="Receiver(s) address. (If you want to use the tranfor_many function, pass \
        the receiver addresses separated by commas)")
parser.add_argument(
    '-a', "--amount", type=int, help="Desired amount to transfer. (In lamports)")
args = parser.parse_args()
try:
    args_receiver = args.receiver
    args_amount = args.amount
    is_valid = True
    if args.func in (Func.TRANSFER, Func.TRANSFER_MANY):
        if not args_receiver or not args_amount:
            print("The --receiver and --amount arguments are required")
            is_valid = False
    if is_valid:
        if args.func == Func.TRANSFER_MANY:
            args_receiver = args_receiver.split(",")
        main(args.func, args.cluster, {
            "receiver": args_receiver,
            "amount": args_amount
        })
except:
    traceback.print_exc()
