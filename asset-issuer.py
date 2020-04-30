from stellar_sdk import Server, Network, Keypair, TransactionBuilder
import json
import requests
import argparse


# Command line interace will come eventually.
# Using argparse for now to allow for command line arguments.
parser = argparse.ArgumentParser(
    description='Create asset with x supply and a basic market using half the supply.')
parser.add_argument('abbreviation', help='Currency code of asset')
parser.add_argument('supply', help='Total supply of asset')
parser.add_argument(
    'market', help='Do you want to make a basic market for your asset? (y\n)')
args = parser.parse_args()

# Declaring global variable for testnet link.
TESTNET = 'https://horizon-testnet.stellar.org'

# Generate random keypairs and funding them with friendbot.
# Side note: It is common to use a Create Account operation to
# handle the cretion of the distributor account (or any account on mainnet).
# I didn't find it necessary to use for this implementation in order to keep the code
# clean and simple.
def generate_keypair():
    friendbot = 'https://friendbot.stellar.org'
    keypair = Keypair.random()
    requests.get(friendbot, params={'addr': keypair.public_key})
    print('Public key: ', keypair.public_key)
    print('Private key: ', keypair.secret, '\n')
    return keypair


# Create a trustline between distributing account and issuing account for asset.
def create_asset(issuing_keypair, distributing_keypair, asset_code):
    # Talk to Horizon testnet instance.
    server = Server(horizon_url=TESTNET)

    # Fetch the current sequence number for the source account from Horizon.
    source_account = server.load_account(distributing_keypair.public_key)

    # Build transaction around trustline operation (creating asset).
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,  # too lazy to fetch :)
        )
        .append_change_trust_op(asset_code, issuing_keypair.public_key)
        .build()
    )

    # Sign transaction with distributor private key.
    transaction.sign(distributing_keypair)

    # Submit signed transaction to Horizon.
    response = server.submit_transaction(transaction)
    print(json.dumps(response, indent=2))

# Send asset from issuing accout to distributing account.
def send_asset(issuing_keypair, distributing_keypair, asset_code, supply):
    # Talk to Horizon testnet instance.
    server = Server(horizon_url=TESTNET)

    # Fetch the current sequence number for the source account from Horizon.
    source_account = server.load_account(issuing_keypair.public_key)

    # Build transaction around payment operation (sending asset to distributor).
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,  # too lazy to fetch :)
        )
        .append_payment_op(distributing_keypair.public_key, supply, asset_code, issuing_keypair.public_key)
        .build()
    )

    # Sign transaction with issuing private key.
    transaction.sign(issuing_keypair)

    # Submit signed transaction to Horizon.
    response = server.submit_transaction(transaction)
    print(json.dumps(response, indent=2))

# Do some magic math to use a portion of the supply to make the market.
# By allowing too big of a market the distributor can run out of lumens;
# this function should solve such issues.
def market_supply(supply):
    if int(supply) > 1000000:
        _supply = int(500000 * 0.15) / 6
    else:
        _supply = int((int(supply) * 0.15) / 6)
    return str(_supply)

# Make bids for the orderbook.
def make_bids(asset_code, issuing_keypair, distributing_keypair, market_supply):
    # Talk to Horizon testnet instance.
    server = Server(horizon_url=TESTNET)

    # Fetch the current sequence number for the source account from Horizon.
    source_account = server.load_account(distributing_keypair.public_key)

    # Build transaction around manage buy offer operation (setting market bids).
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,  # too lazy to fetch :)
        )
        .append_manage_buy_offer_op('XLM', None, asset_code, issuing_keypair.public_key, market_supply, '.08')
        .append_manage_buy_offer_op('XLM', None, asset_code, issuing_keypair.public_key, market_supply, '.09')
        .append_manage_buy_offer_op('XLM', None, asset_code, issuing_keypair.public_key, market_supply, '.10')

        .build()
    )

    # Sign transaction with distributor private key.
    transaction.sign(distributing_keypair)

    # Submit signed transaction to Horizon.
    response = server.submit_transaction(transaction)
    print(json.dumps(response, indent=2))

# Make asks for the orderbook.
def make_asks(asset_code, issuing_keypair, distributing_keypair, market_supply):
    # Talk to Horizon testnet instance.
    server = Server(horizon_url=TESTNET)

    # Fetch the current sequence number for the source account from Horizon.
    source_account = server.load_account(distributing_keypair.public_key)

    # Build transaction around manage sell offer operation (setting market asks).
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,  # too lazy to fetch :)
        )
        .append_manage_sell_offer_op(asset_code, issuing_keypair.public_key, 'XLM', None, market_supply, '.11')
        .append_manage_sell_offer_op(asset_code, issuing_keypair.public_key, 'XLM', None, market_supply, '.12')
        .append_manage_sell_offer_op(asset_code, issuing_keypair.public_key, 'XLM', None, market_supply, '.13')

        .build()
    )

    # Sign transaction with distributor private key.
    transaction.sign(distributing_keypair)

    # Submit signed transaction to Horizon.
    response = server.submit_transaction(transaction)
    print(json.dumps(response, indent=2))


# Encapsulate all that cool stuff up above.
def app(asset_code, supply, market):

    print('\nIssuer Keypair')
    issuer = generate_keypair()

    print('Distributor Keypair')
    distributor = generate_keypair()

    print('Creating asset...')
    create_asset(issuer, distributor, asset_code)

    print('\nSending asset...')
    send_asset(issuer, distributor, asset_code, supply)

    if market == 'y':
        # Take a % of the total supply and use it to make a market
        mkt_supply = market_supply(supply)

        # Create a basic market with half the supply
        print('\nMaking market bids...')
        make_bids(asset_code, issuer, distributor, mkt_supply)

        print('\nMaking market asks...')
        make_asks(asset_code, issuer, distributor, mkt_supply)

    else:
        print('\nNo market made.')

if __name__ == '__main__':
    app(args.abbreviation, args.supply, args.market)
