# gameprices

[![Build Status](https://travis-ci.org/snipem/psnprices.svg?branch=master)](https://travis-ci.org/snipem/psnprices)
[![Coverage Status](https://coveralls.io/repos/github/snipem/psnprices/badge.svg?branch=master)](https://coveralls.io/github/snipem/psnprices?branch=master)

Command line tool for alerting price drops in the Sony PlayStation Network (PSN) and the Nintendo Eshop.

## Description

The Sony Entertainment Network (SEN) uses CIDs to identify items in it's catalogue. In order to alert you on the desired price of an SEN you need the CID. Use your Browser (cid GET parameter in URL) or this script (--search) to retrieve the CID.

In order to check the price of an item. You need a store identifier. These store identifiers are known to work:

* DE/de (Germany)
* GB/en (Great Britain)
* US/en (United States)
* SE/en (Sweden)
* JP/jp (Japan)

Prices are always in the local currency. Therefore it is € for DE/de and £ for GB/en. Additionaly, prices are that for PlayStation Plus users.

### Eshop implementation

The eshop implementation is not yet fully functional and only available in the dvelopment build.

## Installation

Use PyPI to install `psnprices`

    pip install psnprices

This will install the Python modules and also the following command line tools

    psncli
    psnmailalert
    psndealsmailalert

### Install development build

    pip install .

This will also install the beta eshop implementation

    eshopcli
    dealsmailalert

## Usage

### Mail alerting for single alerts you define yourself

Just run `psnmailalert` for mail alerting. See example below. Alerts are set in the `alerts.csv` file. If no store is set. The german / european store is used as a default.

### Command line interface

    usage: psncli [-h] [--id ID] [--store STORE] [--price PRICE] [--query QUERY]
                [--log]

    optional arguments:
    -h, --help            show this help message and exit
    --id ID, -i ID        CID of game to check
    --store STORE, -s STORE
                            Regional PSN store to check. Default: 'DE/de'
    --price PRICE, -p PRICE
                            Desired price of game
    --query QUERY, -q QUERY
                            Name of item to search for
    --log, -l             Write to log file

#### Retrieving UTF-8 encoded output on terminals

You may have to tell Python that your terminal is capable of dealing with UTF-8 outputs. Some PSN items are annotated with trademark, copyright or foreign language specific symbols. To do so set `export PYTHONIOENCODING=utf-8` in your terminal window.

### Mail alerting for collections of price reductions

The PlayStation Network creates collections for price reductions. Run `python psndealsmailalert.py` for watching those collections and be alerted if there are new reductions. Alerts for collections are set in the `alert_deal_containers.csv` file.

## Example

You may run this script with the following command line variants:

### Mail alerting - Get a mail when alerts have been met

With `psnmailalert` you may set alerts for price drops in the `alerts.csv` file. The first value is the CID for the item, the second is the price to be matched in order to alert you by mail, and the second value is the store to search in. You may mix stores in the `alerts.csv`. After a price has been matched, the alert is removed from `alerts.csv`. You will not get any further alerts for that item.

    P0001-NPEJ00305_00-B000000000001030,19.00,DE/de
    P0001-NPEJ00305_00-B000000000001030,19.00,DE/de
    EP0102-CUSA02521_00-MEGAMANLEGACY000,7.00
    UP0102-CUSA02516_00-MEGAMANLEGACY000,7.00,US/en
    P0101-ULES01372_00-GPCMETALGE000001,10.00,DE/de

If the store value is left blank, the script tries to extract the store from the beginning character of the CID.

 In order to receive mails you have to set your account settings in the file `mailconfig.json`. See `mailconfig.json_example` for an example config.

 To run `psnmailalert`, just type:

    psnmailalert

#### Example mail

![Mail with alerts](https://raw.githubusercontent.com/snipem/psnprices/master/res/mail.png "Mail with alerts")

### Searching for the CID of an item

Define the name of a game and the store.

    psncli --query "metal gear solid peace walker" --store DE/de

You will get a result containing one to many search results with the CID. The first output of each search line is the CID, the second the name, the third the supported systems and the last is a description of the item type in the local store language. It is "Vollversion" here which means "full version" in German.

    EP0101-ULES01372_00-GPCMETALGE000001    Metal Gear Solid: Peace Walker  PS Vita,PSP®    9.99    GAME

### Check if desired price has been met

The price is in local currency. As exit statuses render the outcome of the alert, you may send you e-mails or desktop notifications with `&&` or `||`. In this example, there is a string printed to the console.

    psncli --id EP0101-ULES01372_00-GPCMETALGE000001 --store DE/de --price 15.00 &&
    echo "Price matched, let's buy Metal Gear Solid PW"

## Disclaimer

This script is not associated with Sony, Sony PlayStation, the PlayStation Network in any kind. It consumes an public interface that is publicly advertised to the browser to list store contents.

This script is not associated with Nintendo, Nintendo Switch, or the Nintendo Eshop in any kind. It consumes an public interface that is publicly advertised to the browser to list store contents.
