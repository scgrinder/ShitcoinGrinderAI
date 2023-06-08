import configparser
import socket
import sqlite3
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import time
from utils.helpers import get_router_for_network, get_usdt_token_address, to_fixed, get_factory_for_network, DIVIDER
import math
import threading
from datetime import datetime
from statistics import mean

class Client:

    trader = None
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')

        self.auth_token = self.config['Account']['auth_token']
        self.server_host = self.config['Source']['host']
        self.server_port = int(self.config['Source']['port'])
        self.network = self.config['Network']['id']
        self.rpc = self.config['Network']['rpc']
        self.max_trade_size = int(self.config['Trading']['max_trade_size']) / 100
        self.tp = int(self.config['Trading']['take_profit']) / 100
        self.max_position_lifetime = int(self.config['Trading']['position_max_lifetime']) / 100
        self.check_interval = int(self.config['Trading']['check_interval'])

        self.account = Account(self.config['Account']['private_key'], self.rpc)

        self.db_conn = sqlite3.connect('trades.db', check_same_thread=False)
        self.db_cursor = self.db_conn.cursor()

        self.web3 = Web3(HTTPProvider(self.rpc))
        if 'bsc' in self.rpc:
            self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.trader = Trader(self.web3, self.account, get_router_for_network(int(self.network)), get_factory_for_network(int(self.network)))

        self.create_table()
        print(f"\t+ Position Check Interval: {self.check_interval} min")
        print(f"\t+ Position Max Lifetime: {self.max_position_lifetime} days")

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        self.client_socket.send(f"{self.auth_token},{self.account.address},{self.network}".encode())
        response = self.client_socket.recv(1024).decode().strip()
        if(response.upper()) == 'UNAUTHORIZED':
            print("\t+ Source: unauthorized apikey")
            exit(0)
        else:
            print("\t+ Source succesfully connected.")

    def receive_message(self):
        try:
            message = self.client_socket.recv(1024).decode().strip()
            if(len(message) > 0):
                self.execute_message(message)
            print("\t+ Waiting for a signal...")
        except KeyboardInterrupt:
            print("\t+ Connection closed by user.\n")
            print_exit_message()
            exit(0)

    def execute_message(self, message):
        token_from, token_to, amount, network = message.split('/')
        token_from = self.web3.to_checksum_address(token_from.strip())
        token_to = self.web3.to_checksum_address(token_to.strip())
        amount = float(amount)
        network = int(network)

        (from_symbol, from_decimals) = Trader.get_token_info(self.web3, token_from)
        (to_symbol, to_decimals) = Trader.get_token_info(self.web3, token_to)
        print(f"\n\t+ Message received ({time.strftime('%d %b @ %H:%M:%S')}):\n\n\t\t+ from: {from_symbol}({token_from})\n\t\t+ to: {to_symbol}({token_to})\n\t\t+ amount: {min(amount*100, self.max_trade_size*100)}%\n\t\t+ network: {network}")

        if(network != int(self.network)):
            print("\t\t+ Not my network, skip signal.")
            return

        token_balance = self.account.get_balance(token_from, parse=False)
        abs_amount = math.floor(token_balance * min(amount, self.max_trade_size))

        (trade_price, trade_tx) = self.trader.trade(token_from, token_to, abs_amount, self.account.address)
        balance_after = self.account.get_balance(token_from)
        #if(token_from == get_usdt_token_address(self.network)):
        self.log_trade(token_from, token_to, abs_amount, network, trade_price, trade_tx)
        print(f"\t\t+ avg price: {to_fixed(trade_price, 4)} {to_symbol}/{from_symbol}")
        print(f"\t\t+ {from_symbol} paid: {to_fixed(abs_amount * (10**-from_decimals), 4)}({abs_amount})")
        print(f"\t\t+ current balance: {to_fixed(balance_after,4)} {from_symbol}")
        print(f"\t\t+ tx hash: {self.trader.w3.to_hex(trade_tx)}.")
        print(f"\t\t+ Message executed.\n\t{DIVIDER}\n")

    def start(self):
        self.connect_to_server()
        print("\t+ Waiting for a signal...")

        # Create a thread for asset checking
        check_thread = threading.Thread(target=self.run_asset_check, daemon=True)
        check_thread.start()

        while True:
            self.receive_message()
            # self.check_assets_if_needed()
    
    def run_asset_check(self):
        while True:
            self.check_assets()
            time.sleep(self.check_interval * 60)

    def stop(self):
        self.client_socket.close()
        self.db_conn.close()

    def log_trade(self, token_from, token_to, amount, network, trade_price, txid):
        try:
            sql = '''INSERT INTO trades (token_from, token_to, amount, network, trade_price, txid, open_at, closed_at) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
            values = (token_from, token_to, amount, network, trade_price, txid, datetime.now().isoformat(), "")
            self.db_cursor.execute(sql, values)
            self.db_conn.commit()
        except Exception as e:
            print(f"[DB_ERROR] An error occurred in log_trade(): {e}")

    def get_open_trades(self):
        sql = "SELECT * FROM trades WHERE closed_at=''"
        self.db_cursor.execute(sql)
        self.db_conn.commit()
        return self.db_cursor.fetchall()

    def close_trade(self, trade_id):
        sql = '''UPDATE trades SET closed_at=? WHERE id=?'''
        self.db_cursor.execute(sql, (1, datetime.now().isoformat(), trade_id))
        self.db_conn.commit()

    def check_assets(self):
        print("\t+ Checking open positions")
        open_trades = self.get_open_trades()
        print(f"\t\t+ {len(open_trades)} positions to check...")
        for trade in open_trades:
            (id, token_from, token_to, amount, network, trade_price, txid, open_at, closed_at) = trade
            current_price = self.trader.get_token_price_in_usdt(
                get_usdt_token_address(int(self.network)),
                token_to,
            )
            #price_impact = self.trader.calculate_price_impact(token_to, token_from, amount)
            (from_symbol, from_decimals) = self.trader.get_token_info(self.web3, token_from)
            (to_symbol, to_decimals) = self.trader.get_token_info(self.web3, token_to)
            # open=100 current=120 => protif % = (open / (current-open)) * 100
            current_profit_percent = (1 - (trade_price / current_price)) * 100
            print(f"\t\t\t+ Position {from_symbol}/{to_symbol}: open@{to_fixed(trade_price,4)} | current@{to_fixed(current_price,4)} | PL: {to_fixed(current_profit_percent,2)}% | TP@{to_fixed(trade_price * self.tp,4)} ({self.tp*100}%)")
            if current_price >= (trade_price * self.tp):
                print(f"\t\t\t+ [TP] Closing {token_to}: ...")
                token_balance = self.account.get_balance(token_to, parse = False)
                self.trader.trade(token_to, token_from, token_balance, self.account.address)
                self.close_trade(id)
                print(f"\r\t\t\t+ [TP] Closing {token_to}: {txid}")
            elif (datetime.now() - datetime.fromisoformat(open_at)).days >= 30:
                print(f"\t\t\t+ [EXPIRED] Closing {token_to}: ...")
                token_balance = self.account.get_balance(token_to, parse = False)
                self.trader.trade(token_to, token_from, token_balance, self.account.address)
                self.close_trade(id)
                print(f"\r\t\t\t+ [TP] Closing {token_to}: {txid}")
                
        print(f"\t\t+ Done, next check in {self.check_interval} minutes\n")
    
    def create_table(self):
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS trades 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             token_from TEXT,
             token_to TEXT,
             amount FLOAT,
             network INTEGER,
             trade_price FLOAT,
             txid TEXT,
             open_at TEXT,
             closed_at TEXT)''')
        self.db_conn.commit()

# Account class
class Account:
    def __init__(self, private_key, rpc):
        self.private_key = private_key
        self.rpc = rpc
        self.w3 = Web3(HTTPProvider(rpc))
        self.account = self.w3.eth.account.from_key(private_key)

    @property
    def address(self):
        return self.account.address

    def get_balance(self, token_address, parse=True):
        contract_abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}, {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"decimals","outputs":[{"name":"decimals","type":"uint256"}],"type":"function"}]'
        contract_abi = [
            {"constant": "true","inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable": "false","stateMutability":"view","type":"function"},
            {"constant": "true","inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":  "false","stateMutability":"view","type":"function"}
        ]
        token_contract = self.w3.eth.contract(address=self.w3.to_checksum_address(token_address), abi=contract_abi)
        balance = token_contract.functions.balanceOf(self.address).call()
        if parse:
            decimals = token_contract.functions.decimals().call()
            return balance * (10 ** -decimals)
        else:
            return balance

# Trader class
class Trader:
    def __init__(self, web3, _account, router_address, factory_address):
        self.account = _account
        self.rpc = _account.rpc
        self.router_address = router_address
        self.w3 = web3
        self.factory_address = factory_address

    def trade(self, token_in, token_out, amount_in, to, deadline=0, slippage_tolerance=0.1):
        if deadline == 0:
            deadline = int(time.time()) + 300
        router_abi = [
            {"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},
            {"anonymous": "false", "inputs": [{"indexed": "true", "internalType": "address", "name": "sender", "type": "address"}, {"indexed": "false", "internalType": "uint256", "name": "amount0In", "type": "uint256"}, {"indexed": "false", "internalType": "uint256", "name": "amount1In", "type": "uint256"}, {"indexed": "false", "internalType": "uint256", "name": "amount0Out", "type": "uint256"}, {"indexed": "false", "internalType": "uint256", "name": "amount1Out", "type": "uint256"}, {"indexed": "true", "internalType": "address", "name": "to", "type": "address"}], "name": "Swap", "type": "event"}
        ]
        router = self.w3.eth.contract(address=self.router_address, abi=router_abi)

        path = [token_in, token_out]
        path = [self.w3.to_checksum_address(address) for address in path]
        amounts_out = router.functions.getAmountsOut(amount_in, path).call()
        ideal_amount_out = amounts_out[-1]

        slippage_amount = ideal_amount_out * slippage_tolerance / 100
        amount_out_min = math.floor(ideal_amount_out - slippage_amount)

        self.approve_if_needed(token_in, amount_in, self.router_address)

        amount_before = self.account.get_balance(token_out, parse=False)
        tx = router.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            amount_in,
            amount_out_min,
            path,
            to,
            deadline
        ).build_transaction({
            'from': self.account.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.account.address),
            'gas': 2000000,
            'gasPrice': self.w3.to_wei('5', 'gwei')
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.private_key)

        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

        amount_after = self.account.get_balance(token_out, parse=False)
        avg_price = amount_in / (amount_after - amount_before)

        return (avg_price, tx_hash)

    def approve_if_needed(self, token_address, amount, router_address):
        token_abi = [
            {"constant": True, "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "remaining", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
            {"constant": False, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"}
        ]
        
        token = self.w3.eth.contract(address=token_address, abi=token_abi)
        allowance = token.functions.allowance(self.account.address, router_address).call()
        if allowance < amount:
            print("\t+ Approve necessary! Approving...")
            tx = token.functions.approve(router_address, amount*1000).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 2000000,
                'gasPrice': self.w3.to_wei('5', 'gwei')
            })

            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"\t+ Approved. {str(tx_receipt['transactionHash'])}")

    @staticmethod
    def get_token_info(web3, token_address):
        token_abi = [
            {"constant":"true","inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":"false","stateMutability":"view","type":"function"},
            {"constant":"true","inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":"false","stateMutability":"view","type":"function"}
        ]
        token = web3.eth.contract(address=web3.to_checksum_address(token_address), abi=token_abi)
        symbol = token.functions.symbol().call()
        decimals = token.functions.decimals().call()
        return (symbol, decimals)

    def get_reserves(self, token_in, token_out):
        factory_abi = [
            {"constant":"true","inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":"false","stateMutability":"view","type":"function"}
        ]
        pair_abi = [
            {"constant":"true","inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":"false","stateMutability":"view","type":"function"}
        ]

        factory = self.w3.eth.contract(address=self.factory_address, abi=factory_abi)
        pair_address = factory.functions.getPair(self.w3.to_checksum_address(token_in), self.w3.to_checksum_address(token_out))
        pair = self.w3.eth.contract(address=pair_address, abi=pair_abi)
        return pair.functions.getReserves()[:2]

    def calculate_price_impact(self, token_in, token_out, swap_amount):
        (reserve_in, reserve_out) = self.get_reserves(token_in, token_out)
        price_impact = (swap_amount / (reserve_in - swap_amount)) * 100
        return price_impact

    def get_token_price_in_usdt(self, usdt, token):
        router_abi = [
            {"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},
            {"anonymous": "false", "inputs": [{"indexed": "true", "internalType": "address", "name": "sender", "type": "address"}, {"indexed": "false", "internalType": "uint256", "name": "amount0In", "type": "uint256"}, {"indexed": "false", "internalType": "uint256", "name": "amount1In", "type": "uint256"}, {"indexed": "false", "internalType": "uint256", "name": "amount0Out", "type": "uint256"}, {"indexed": "false", "internalType": "uint256", "name": "amount1Out", "type": "uint256"}, {"indexed": "true", "internalType": "address", "name": "to", "type": "address"}], "name": "Swap", "type": "event"}
        ]
        (symbol, decimals) = Trader.get_token_info(self.w3, token)
        router = self.w3.eth.contract(address=self.router_address, abi=router_abi)
        path = [self.w3.to_checksum_address(usdt), self.w3.to_checksum_address(token)]
        amounts_out = router.functions.getAmountsOut(10**18, path).call()
        return mean([ 1 / (amounts_out[-1] * (10**-decimals))])

def print_exit_message():
    print("\n==== IMPORTANT =====")
    print("\nShitCoinGrinderAI+ won't be free forever.\nWhen access to SCGrinderAI+ is revoked, only those who have actively contributed to improving the software will be able to get an ultimate premium account.\nFor any issues and/or feedback, please refer to issues@shitcoingrinder.io\n")

# Main program
if __name__ == '__main__':
    print("\n==== ShitCoinGrinderAI+ =====\n")
    client = Client()
    client.start()
