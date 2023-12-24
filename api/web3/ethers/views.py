from rest_framework.views import APIView
from utils.response import CustomResponse
from web3 import Web3, Account
from web3.middleware import construct_sign_and_send_raw_middleware
import os

class EthersFundView(APIView):
    def post(self, request, format=None):
        try:
            w3 = Web3(Web3.HTTPProvider(os.environ.get('BLOCKCHAIN_URL')))
            funderKey = os.environ.get('FUNDER_ACCOUNT')
            account = Account.from_key(funderKey)
            w3.eth._chain_id
            to_address = request.data.get('to_address') 
            to_address = w3.to_checksum_address(to_address)
            amount_required = w3.to_wei(0.2, 'ether')
            r_balance = w3.eth.get_balance(to_address)
            if (amount_required <= r_balance):
                return CustomResponse("Already have enough funds!").send_success_response()
            amount_to_send = amount_required - r_balance
            print("Sending ",w3.from_wei(amount_to_send,"ether")," ether to ",to_address)
            transaction = {
                'from': account.address,
                'to': to_address,
                'value': amount_to_send,
                'nonce': w3.eth.get_transaction_count(account.address),
                'gas': 200000,
                'maxFeePerGas': 2000000000,
                'maxPriorityFeePerGas': 1000000000,
                "chainId":1337
            }
            
            signed = w3.eth.account.sign_transaction(transaction, funderKey)
            tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
            tx = w3.eth.get_transaction(tx_hash)
            assert tx["from"] == account.address
            print(f"Transaction successful with hash: {tx_hash.hex()}")
            bal = w3.from_wei(w3.eth.get_balance(to_address),"ether")
            return  CustomResponse(
                message="Ethers Fund",
                data={
                    'message': 'Ethers Fund',
                    'data': {
                        "transaction":tx_hash.hex(),
                        "balance": bal
                    }
                }
            ).send_success_response()
        except Exception as e:
            print(e)
            return CustomResponse("Error Occured while funding account!").send_failure_response(400)