## Getting Started

First, install required packages:

```bash
python -m venv app/venv
source venv/bin/activate
pip install -r requirements.txt
```
Copy .env.example to .env and fill the parameters.

- SECRET_KEY is your wallet's private key for signing transactions.
- LOCAL_WALLET_PATH is used for testing on localnet.

## Use the client

First, activate the virtual environment.

```bash
source venv/bin/activate
```

To communicate with the program (contract) use the following commands.

- Transfer lamports to an account

  ```bash
  python main.py transfer testnet -r [Receiver address] -a [Amount]
  ```
  
- Transfer lamports to multiple accounts

  ```bash
  python main.py transfer_many testnet -r [Receiver addresses] -a [Amount]
  ```

- Initialize The Program

  ```bash
  python main.py initialize devnet
  ```

- Increment counter

  ```bash
  python main.py increment devnet
  ```

You can use the following command to learn more about commands.

```bash
python main.py -h
```
