from typing import Sequence, Any, Tuple
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import transfer, transfer_many, TransferParams
from solana.transaction import Transaction
from solana.rpc.api import Client
from solana.exceptions import SolanaExceptionBase
from solana.rpc.core import RPCException


class SolanaClient:

    def __init__(self, rpc_client: Client, signer: Keypair) -> None:
        self.rpc_client = rpc_client
        self.signer = signer

    def call_program(self, program_id: Pubkey, data: Any, accounts: Sequence[AccountMeta]):

        from_pubkey = Pubkey.from_string(
            "6ZWcsUiWJ63awprYmbZgBQSreqYZ4s6opowP4b7boUdh")
        user_pubkey = Pubkey.from_string(
            "6ZWcsUiWJ63awprYmbZgBQSreqYZ4s6opowP4b7boUdh")
        program_id = "program-id"
        accounts = [AccountMeta(from_pubkey, is_signer=True, is_writable=True),
                    AccountMeta(user_pubkey, is_signer=False, is_writable=True)]
        data = [{"to": user_pubkey, "amount": 100}]
        instruction = Instruction(program_id, bytes(data), accounts)
        txn = Transaction().add(instruction)

        base58_str = "1" * 64
        self.rpc_client.send_transaction(
            txn, Keypair.from_base58_string(base58_str))

    def transfer_lamports(self, sender: Pubkey, receiver: Pubkey, amount: int):
        instruction = transfer(
            TransferParams(from_pubkey=sender,
                           to_pubkey=receiver, lamports=amount)
        )
        txn = Transaction().add(instruction)

        try:
            self.rpc_client.send_transaction(txn, self.signer)
        except SolanaExceptionBase as exc:
            print(exc.error_msg)

    def transfer_many_lamports(self, sender: Pubkey, receivers: Sequence[Tuple[Pubkey, int]]):
        txn = Transaction()
        for rec in receivers:
            instruction = transfer(
                TransferParams(from_pubkey=sender,
                               to_pubkey=rec[0], lamports=rec[1])
            )
            txn.add(instruction)

        try:
            self.rpc_client.send_transaction(txn, self.signer)
        except SolanaExceptionBase as exc:
            print(exc.error_msg)
        except RPCException as exc:
            print(exc)
