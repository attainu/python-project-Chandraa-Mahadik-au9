Project Title: 
Bitcoin Price Notification 

Description:
The project includes Notifying the user on Telegram for price of Bitcoin specifically and optionally notification of Ethereum. Choices will be provided on the command line.
BTC : Bitcoin
ETH: Ethereum

There will be notifications on regular interval for the choice of cryptocurrency made.
Also there will be an emergency notification for the user in case if the price of BTC / ETH goes below a spefied threshold price provided.
Say BTC threshold = $ 10K.
and ETH threshold = $ 300.


Table of contents:

Code file:
btc_notification.py

README.md


Installation:

Python library:
flake8
Vscode
IFTTT Account

Telegram App
Gmail App
and modules specified in the section below.

Usage Instructions:

1. Run the code in command line.
2. Provide all the arguments needed. 
3. Arguments:
    'BTC' = For Bitcoin.
    'ETH' = For Ethereum.

4. Provide a threshold price for both curriencies:
    BTC threshold may be $10000 and ETH threshold may be $300.

5. Last argument to provide is notification time interval:
    Say about 5 mins or any speecific time input in minutes.

The Notifications will be sent to Telegram App and a mail will be sent to gmail account of the user.