# Automated Token Sale

The automated token sale is the first big example in the radixlib which is built to showcase the power of this package and what its capable of.

Since smart contracts are not currently live on the Radix network, many NFT projects and new tokens launching on the Radix ledger end up performing a manual token sale where after an X amount of XRD is sent to the creators, Y amount of tokens are sent to the buyer. As you might imagine, this manual process takes time and is very prone to human errors. 

It goes without saying that this process of exchanging XRD tokens for some other token seems like a very simple task and one which might be very easy to automate. Therefore, in this example we build an automated token sale script for an imaginary token on the Radix blockchain called "Bitcoin". 

Here are some of the features of this automated token sale script:

* Automates the process of token sales.
* Allows for sales to happen instantaneously.
* Performs automatic refunds for other tokens sent and excess XRD.

## Getting Started

This section of the document outlines the process and steps which you need to carry out to begin using this script.

### Step 1: Installing the RadixLib Package

The first thing which you will need to do is to install the radixlib python package to your current python interpreter. The steps for installing the radixlib package have been documented [here](https://github.com/0xOmarA/RadixLib#installing-the-package).

### Step 2: Edit the `config.py` file.

The config.py file contains a lot of important information used by the script for the token creation and also for the sale. You will need to edit the config.py file so that it has the information of token that you're trying to sell as well as the mnemonic phrase of the wallet that you want to listen for transactions on. So, you will need to edit the following variables:

* `network`: Change the network to the network which you wish to connect to and use. This currently defaults to the stokenet (testnet) and not the mainnet.
* `mnemonic_phrase`: The mnemonic phrase of the wallet that you want to listen for transactions on (this is the wallet that people will be sending funds to).
* `token_*`: The token information variables need to be edited with information about the token you're trying to create.
* `token_price_in_atto`: This is the price of tokens in atto. You may use the `radix.derive.atto_from_xrd` function to find how much atto is in the XRD price you'd like to set. This defaults to 20 XRD; meaning that 1 of our imaginary Bitcoin tokens is worth 20 XRD.

### Step 3: Create the Token (Optional)

This step is optional if you have already created the token specified in the `config.py` file. If you have not yet created it, then you may follow the steps outlined here. 

First of all, I'm assuming that you currently have all of the files from this example in your current working directory, such that running `ls` in your current directory outputs the following:

```shell
$ ls
README.md               config.py               creating token.py       data.json               token sale.py
```

You may also have an `env` directory in there if you're running python inside of a virtual environment. 

With steps 1 and 2 already completed, you may now run the following command to create your token if it does not already exist:
```shell
python3 "creating token.py"
```

Check the output in the command line to make sure that there are no errors that happened or no exceptions. Correct operation of the script would read something like:
```
Token creation in transaction: c850b856d0edcabc933467e9361112d95cfb1adef51f2b117aa0830d5d6d3ad7
```

### Step 4: Running your Automated Sale

We are now finally ready to run the automated sale of the tokens. One important thing to note is that the code in the `token sale.py` file does not use while loops or anything of that sort to keep the code running. Instead, you're expected to use cronjobs (or other similar methods) to make this script run periodically to check for new transactions and perform the sale or refund of tokens. 

So, let's create a cronjob for this script to make it run once every 2 minutes. To create that cronjob, run the following commands:
```shell
crontab -l >> mycron
echo "*/2 * * * * \"$(which python3)\" \"$(pwd)/token sale.py\" >> \"$(pwd)/log.log\"" >> mycron
crontab mycron
rm mycron
```

Viola! Now your automated token sale is happening! Every 2nd minute (x:00, x:02, x:04) your code runs, checks for new transactions on your wallet address, and sends the tokens out!