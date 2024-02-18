from web3 import Web3, AsyncWeb3
import json, requests
from eth_account import Account

web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

adminAccount = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'
adminAccount = Account.from_key(adminAccount)
accounts = [Account.create() for _ in range(10)]

candidate_abi = json.loads(open('./contracts/Candidate.abi.json', 'r').read())
voter_abi = json.loads(open('./contracts/Voter.abi.json', 'r').read())
voter_reader_abi = json.loads(open('./contracts/VoterReader.abi.json', 'r').read())
votechain_abi = json.loads(open('./contracts/Votechain.abi.json', 'r').read())

voter_data = json.loads(open('./voter-data.json', 'r').read())

res = requests.get('https://votechain-backend.vercel.app/api/system/config')
data = json.loads(res.text)['data'][0]

candidate_address = data['candidateAddress']
voter_address = data['voterAddress']
voter_reader_address = data['voterReaderAddress']
votechain_address = data['votechainAddress']

Candidate = web3.eth.contract(abi=candidate_abi, address=candidate_address)
Voter = web3.eth.contract(abi=voter_abi, address=voter_address)
VoterReader = web3.eth.contract(abi=voter_reader_abi, address=voter_reader_address)
Votechain = web3.eth.contract(abi=votechain_abi, address=votechain_address)

if web3.is_connected():
    print('Connected to Ethereum')
    print(' # Registering 10 voters ')
    for i in range(0,10):
        requests.post('http://localhost:8000/api/web3/ethers/fund/',{'to_address': accounts[i].address})
        print(f'  - Registering voter {i+1} : {accounts[i].address}')
        transaction = Voter.functions.registerVoter(voter_data[i],'284fa10c-9684-4e8e-a0ff-e45954d06cc4').build_transaction({'from': accounts[i].address,'nonce': web3.eth.get_transaction_count(accounts[i].address)})
        transaction = web3.eth.account.sign_transaction(transaction, private_key=accounts[i].key)
        tx_hash = web3.eth.send_raw_transaction(transaction.rawTransaction)
        print(f'    - Transaction Hash : {tx_hash.hex()}')
        requests.post('http://localhost:8000/api/user/auth/register/', json={
            'uid': voter_data[i][0],
            'aadhar': voter_data[i][0],
            'enc1': voter_data[i][1],
            'enc2': voter_data[i][2],
            'voterAddress': accounts[i].address
        })

else:
    print('Could not connect to Ethereum')