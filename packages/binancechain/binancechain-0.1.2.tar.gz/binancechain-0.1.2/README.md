# binance-chain-python

[![Build Status](https://travis-ci.org/lmacken/binance-chain-python.svg?branch=master&color=green)](https://travis-ci.org/lmacken/binance-chain-python)
[![Coverage Status](https://coveralls.io/repos/github/lmacken/binance-chain-python/badge.svg)](https://coveralls.io/github/lmacken/binance-chain-python)
![GitHub](https://img.shields.io/github/license/lmacken/binance-chain-python.svg)
![PyPI](https://img.shields.io/pypi/v/binancechain.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/binancechain.svg)

An unofficial asyncio Python API for the Binance Chain.

## Installation

    pip install binancechain

## Implementation Details

- [Extensive test suite](https://github.com/lmacken/binance-chain-python/tree/master/test)
- [aiohttp](https://aiohttp.readthedocs.io) for all HTTP requests, which automatically performs connection-pooling
- [SPDX license identifiers](https://spdx.org/)
- Python [type hints](https://docs.python.org/3/library/typing.html) for ease of development
- Python3.6+ f-strings for faster string interpolation
- Exception-chaining with [`raise from`](https://docs.python.org/3/library/exceptions.html#built-in-exceptions)
- Clean and consistent syntax formatting with [Black](https://github.com/ambv/black)
- Example CLI tool that just outputs raw JSON responses (`python -m binancechain.cli`)

### Utilizes popular crypto libraries
- [bitcoinlib](https://github.com/1200wd/bitcoinlib)
- [bech32](https://github.com/sipa/bech32)
- [secp256k1](https://github.com/ludbb/secp256k1-py)
- [eth_keyfile](https://github.com/ethereum/eth-keyfile)

### WebSocket

- Decorator and callback API for simple WebSocket usage
- Automatically sends `keepAlive` messages every 30 minutes
- Event-driven using [pyee](https://github.com/jfhbrook/pyee)

## API SECTIONS

- [REST API](https://github.com/lmacken/binance-chain-python#rest-api)
- [NODE RPC](https://github.com/lmacken/binance-chain-python#node-rpc)
- [WEBSOCKET](https://github.com/lmacken/binance-chain-python#websocket-1)
- [WALLET](https://github.com/lmacken/binance-chain-python#binance-chain-wallet)
- [TRANSACTION](https://github.com/lmacken/binance-chain-python#binance-chain-transaction)
------------------

## REST API

### Query information
```python
client = HTTPClient(testnet=True)

server_time = await client.get_time()

node_info = await client.get_node_info()

validators = await client.get_validators()

peers = await client.get_peers()

account_info = await client.get_account_info(address)

sequence_info = await client.get_account_sequence(address)

transaction = await client.get_transaction(hash)

token_list = await client.get_token_list()

markets = await client.get_markets(limit=500, offset=0)

fees = await client.get_fees()

depth = await client.get_depth(symbol, limit=100)

klines = await client.get_klines(symbol, interval, limit=300, start=None, end=None)

closed_orders = await client.get_closed_orders(
    address,
    end=None,
    limit=None,
    offset=None,
    side=None,
    start=None,
    status=None,
    symbol=None,
    total=None,
)

open_orders = await client.get_open_orders(
    self, address, limit=None, offset=None, symbol=None, total=None
)

order = await client.get_order(id)

ticker = await client.get_ticker(symbol)

trades = await client.get_trades(
    address=None,
    buyerOrderId=None,
    height=None,
    limit=None,
    offset=None,
    quoteAsset=None,
    sellerOrderId=None,
    side=None,
    start=None,
    end=None,
    total=None,
    symbol=None,
)

block_fee = await client.block_exchange_fee(
    address=None, end=None, limit=None, offset=None, start=None, total=None
)

transactions = await client.get_transactions(
    address,
    height=None,
    end=None,
    limit=None,
    offset=None,
    side=None,
    start=None,
    tx_asset=None,
    tx_type=None,
)
```
### Broadcast transaction
```python
broadcast_info = await client.broadcast(hash)

```

------------------

## NODE RPC
### Query Information
```python
noderpc = NodeRPC(testnet=True)

abic_info = await noderpc.get_abci_info(path, data=None, height="0", prove=False)

concensus_state = await noderpc.get_consensus_state()

dump_concensus_state = await noderpc.get_dump_consensus_state()

genesis = await noderpc.get_genesis()

health = await noderpc.get_health()

net_info = await noderpc.get_net_info()

status = await noderpc.get_status()

query = await noderpc.abci_query("/param/fees")

block = await noderpc.block(height=None)

block_hash = await noderpc.block_by_hash(hash)

block_results = await noderpc.block_results(height=None)  # ABCIResults

blockchain = await noderpc.blockchain(min_height, max_height)

concensus_params = await noderpc.consensus_params("1")

validators = await noderpc.validators(height=None)

transaction = await noderpc.tx(txid, prove=False)

tx_search = await noderpc.tx_search(query, prove=False, page=1, per_page=30)

pending_transactions = await noderpc.unconfirmed_txs(limit=None)

pendings_number = await noderpc.get_num_unconfirmed_txs()
```
### Broadcast transaction
```python
tx_hash = await noderpc.broadcast_tx_async(hash)

tx_onchain = await noderpc.broadcast_tx_sync(hash)

tx_confirmed = await noderpc.commit(height=None)
```
-------------------

## WEBSOCKET

### Decorator API

```python
from binancechain import WebSocket

dex = WebSocket(address, testnet=True)

@dex.on("open")
async def on_open(): …

@dex.on("allTickers", symbols=["$all"])
async def on_ticker(msg): …

@dex.on("kline_1m", symbols=["000-0E1_BNB"])
async def on_kline(kline): …

@dex.on("orders")
async def user_orders(msg): …

@dex.on("accounts")
async def user_accounts(msg): …

@dex.on("transfers")
async def user_transfers(msg): …

@dex.on("error")
async def on_error(msg): …

dex.start() # or dex.start_async() coroutine
```
### Callback API
```python
from binancechain import WebSocket

dex = WebSocket(address, testnet=True)

def on_open():
    dex.subscribe_user_orders(callback=user_orders)
    dex.subscribe_user_accounts(callback=user_accounts)
    dex.subscribe_user_transfers(callback=user_transfers)

dex.start(on_open, on_error)
```

See the WebSocket [examples](https://github.com/lmacken/binance-chain-python/tree/master/examples) for more information.

----------------

## BINANCE CHAIN WALLET

### Create or recover wallet and keystore
```python
from binancechain import Wallet

wallet = Wallet.create_wallet(password="", testnet=False)

wallet = Wallet.create_wallet_mnemonic(language="english", password="", testnet=False)

keystore = Wallet.create_keystore(password=None)

wallet = Wallet(key="HDKEY object", testnet=False)

wallet = Wallet.wallet_from_keystore(keystore=keystore, password="", testnet=False)

wallet = Wallet.wallet_from_mnemonic(words="mnemonic words", password="", testnet=False)

wallet = Wallet.wallet_from_privatekey(privatekey="private_key", password="", testnet=False)
```

### Using the wallet
```python
from binancechain import Wallet

wallet = Wallet.create_wallet(password="", testnet=True)

address = wallet.get_adress()

priv = wallet.get_privatekey()

pub = wallet.get_publickey()

pub, signature = wallet.sign(msg)

is_valid = wallet.verify_signature(msg, signature)
```

-------------------

## BINANCE CHAIN TRANSACTION

### Using Transaction with wallet and client, handle signing and broadcast internally
```python
from binancechain import Transaction, Wallet

from binancechain.enums import ORDERTYPE, SIDE, TIMEINFORCE, VOTES

#if client is passed in , testnet arg will be ignored

transaction = Transaction(wallet=wallet, client=None,testnet=False)

transfer = await transaction.transfer(to_address, symbol, amount)

broadcast_info = await transaction.create_new_order(
    symbol="binance_pair",
    side=SIDE.Buy,
    ordertype=ORDERTYPE.Limit,
    price=1,
    quantity=1,
    timeInForce=TIMEINFORCE.GTE,
)

broadcast_info = await transaction.cancel_order(symbol="pair", refid)

broadcast_info = await transaction.freeze_token(symbol="token", amount)

broadcast_info = await transaction.unfreeze_token(symbol="token", amount)

broadcast_info = await transaction.vote(
    proposal_id="", option=VOTES.Yes
)
```
### Create Transaction Message. This message can be signed and broadcast somewhere else

```python
limit_buy_transaction = await Transaction.new_order_transaction(
      address="owner address",
      symbol="pair",
      side=SIDE.Buy,
      ordertype=ORDERTYPE.Limit,
      price=1,
      quantity=1,
      timeInForce=TIMEINFORCE.GTE,
      account_number= None,
      sequence= None,
      client= None,
      testnet = False, # will be ignored if client is passed in
  )

limit_sell_transaction = await Transaction.new_order_transaction(
    address="owner address",
    symbol="pair",
    side=SIDE.Buy,
    ordertype=ORDERTYPE.Limit,
    price=1,
    quantity=1,
    timeInForce=TIMEINFORCE.GTE,
    account_number= None,
    sequence= None,
    client= None,
    testnet = False, # will be ignored if client is passed in
)

cancel_order_transaction = await Transaction.cancel_order(
    address="owner_address",
    symbol="pair",
    refid="",
    account_number= None,
    sequence= None,
    client= None,
    testnet = False, # will be ignored if client is passed in
)

freeze_token_transaction = await Transaction.freeze_token(
    address="ownder_address",
    symbol="token",
    amount=1,
    account_number= None,
    sequence= None,
    client= None,
    testnet = False, # will be ignored if client is passed in
)

unfreeze_token_tranasaction = await Transaction.unfreeze_token_transaction(
    address="ownder_address",
    symbol="token",
    amount=1,
    account_number= None,
    sequence= None,
    client= None,
    testnet = False, # will be ignored if client is passed in
)
```
- Example transaction message :

```
b'{"account_number":"668107","chain_id":"Binance-Chain-Nile","data":null,"memo":"","msgs":[{"inputs":[{"address":"tbnb1r5jc35v338tlphnjx65wy7tecm6vm82tftfkt7","coins":[{"amount":10000000,"denom":"BNB"}]}],"outputs":[{"address":"tbnb1nhvpuq0u5pgpry0x2ap2hqv9n5jfkj90eps6qx","coins":[{"amount":10000000,"denom":"BNB"}]}]}],"sequence":"35","source":"1"}'
```

----------------------

## Running the test suite

```bash
git clone https://github.com/lmacken/binance-chain-python.git
pip install -r test-requirements.txt`
python setup.py develop
pytest
```

----------------------

## Contributors

[@lmacken](https://github.com/lmacken)
[@propulsor](https://github.com/propulsor)

## Donate

BNB: `bnb1qx8u39hqcykjy5puv582gvqy5520dsz7fdh9ak`

BTC: `39n2J2hWY5FHCnGwNgRSZTe4TdFKcQea9v`
