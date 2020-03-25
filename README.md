# Asset Issuer Script

Python script that issues an asset on the Stellar testnet and creates a distributor account and a simple market. 

## Why is this useful? 

One of the issues I've seen new Stellar developers run in to is creating new assets and markets. The reason it's tricky is due to the overhead that comes with some of the steps. What is an anchor? What is an issuing account and how is that different than a distrubtor account? What is a trustline? How the heck do I make a market? 

This script aims to make all of that more clear through the code, comments, and this README. 

## What does it do? 

The steps this script goes through are as follows: 
- Create ```Issuing Account``` + fund with testnet lumens 
- Create ```Distributor Account``` + fund with testnet lumens
- Create trustline from ```Distributor Account``` to Issuing Account for ```Asset X```
- Send ```Supply``` from ```Issuing Account``` to ```Distributor Account```
- Create ```Buy Offers``` for ```Asset X``` using 1/4 of the ```Supply``` in ```Distributor Account```
- Create ```Sell Offers``` for ```Asset X``` using 1/4 of the ```Supply``` in ```Distributor Account```


