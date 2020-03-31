# Stellar Asset Issuer Script

Python script that issues an asset on the Stellar testnet and creates a distributor account and a simple market. 

## Why is this useful? 

One of the issues I've seen new Stellar developers run in to is creating new assets and markets. The reason it's tricky is due to the overhead that comes with some of the steps. What is an anchor? What is an issuing account and how is that different than a distrubtor account? What is a trustline? How the heck do I make a market? 

This script aims to make all of that more clear through the code, comments, and this README. 

Really quick, here's some terms to know: 

**```Trustline```** - Establishment of trust between two accounts for an asset. Account A *trusts* an Issuing Account to issue an asset. After *trusting* an account for an asset (e.g. KUSD), the account can receive that asset. 

**```Issuing Account```** - Account responsible for issuing the asset it is trusted for. Let's say Bank of Kolten wants to issue KoltenUSD (KUSD). All users who want to hold KoltenUSD have to trust **my issuing account** for KUSD in order to receive it and verify that they are getting the real KUSD. 

**```Distributor Account```** - Account responsible for distributing the asset. This is the second account owned by Bank of Kolten and is responsible for sending KUSD to users. This seperates the logic between issuing an asset and distributing an asset, along with providing transparency in to the ```Supply```. 

**```Supply```** - An ```Asset's``` total ```Supply``` is the amount of that ```Asset``` in circulation on Stellar. ```Issuing Accounts``` essentially hold an infinite ```Supply``` so it is not tracked until an ```Asset``` is sent from the ```Issuing Account``` to another account. That's why it's important to have a ```Distributor Account```!

**```Asset```** - 

**```Buy Offers```** - 

**```Sell Offers```** - 

## What does it do? 

The steps this script goes through are as follows: 
- Create ```Issuing Account``` + fund with testnet lumens 
- Create ```Distributor Account``` + fund with testnet lumens
- Create trustline from ```Distributor Account``` to Issuing Account for ```Asset X```
- Send ```Supply``` from ```Issuing Account``` to ```Distributor Account```
- Create ```Buy Offers``` for ```Asset X``` using 1/4 of the ```Supply``` in ```Distributor Account```
- Create ```Sell Offers``` for ```Asset X``` using 1/4 of the ```Supply``` in ```Distributor Account```

Here's an example of an asset called ```TEST``` with a supply of ```1,000``` and an active market. 

<div align="center"><img align="center" src="test-asset-details.PNG"></div>
<br>
<div align="center"><img align="center" src="test-asset-orderbook.PNG"></div>
<br>

## Nice, how do I use it? 

Using the script is pretty simple by design but there are a couple of requirements. 
- You must have Python installed. 
- The Stellar Python SDK (newest version) must be installed: ```pip install stellar-sdk```

To actually run the script you compile it as you normally would but include 3 commandline arguments: <br>
```python argparse.py TOKEN_CODE SUPPLY y```
- ```TOKEN_CODE``` is an identifier for your asset (e.g. USD)
- ```SUPPLY``` is the total supply of your asset (e.g. 100) 
- ```y``` specifies that you want to create a market for the asset. Any other input prevents the market from being made. 

Example: <br> 
```python argparse.py TEST 1000 y```
