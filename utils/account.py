from web3 import Web3, HTTPProvider

class Account:
    def __init__(self, private_key, rpc):
        self.w3 = Web3(HTTPProvider(rpc))
        self.account = self.w3.eth.account.privateKeyToAccount(private_key)

    @property
    def address(self):
        return self.account.address

    def get_balance(self, token_address):
        # Assuming it's an ERC20 Token
        contract_abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}, {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"decimals","outputs":[{"name":"decimals","type":"uint256"}],"type":"function"}]'
        token_contract = self.w3.eth.contract(address=token_address, abi=contract_abi)
        balance = token_contract.functions.balanceOf(self.address).call()
        decimals = token_contract.functions.decimals(self.address).call()
        return balance * (10 ** -decimals)
