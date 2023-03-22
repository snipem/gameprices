# Gameprices

[![Build](https://github.com/snipem/psnprices/actions/workflows/build.yaml/badge.svg)](https://github.com/snipem/psnprices/actions/workflows/build.yaml)

Command line tool for alerting price drops in the Sony PlayStation Network (PSN) and the Nintendo Eshop.

## Description

**Since the PSN upgrade that came with the release of PlayStation 5, some functionality of the PSN interface is broken. Currently only searching by a name query is working**

The Sony Entertainment Network (SEN) uses CIDs to identify items in its catalogue. In order to alert you on the desired price of an SEN you need the CID. Use your Browser (cid GET parameter in URL) or this script (`--query`) to retrieve the CID.

In order to check the price of an item. You need a store identifier. These store identifiers are known to work:

* DE/de (Germany)
* GB/en (Great Britain)
* US/en (United States)
* SE/en (Sweden)
* JP/jp (Japan)

Prices are always in the local currency. Therefore, it is € for DE/de and £ for GB/en. Additionally, prices are those for PlayStation Plus users.

The Eshop implementation lacks unique identifiers, because the Eshop does not support searching for unique identifiers. Therefore, an identifier is constructed containing the game name.

## Installation

Use PyPI to install `gameprices`

```bash
pip install gameprices
```

This will install the Python modules and also the following command line tools

```
psncli
eshopcli
psnmailalert
dealsmailalert
```

### Install development build

```bash
pip install .
```

## Usage

### Mail alerting for single alerts you define yourself

Just run `psnmailalert` for mail alerting. See example below. Alerts are set in the `alerts.csv` file. If no store is set. The German / European store is used as a default.

### Command line interface

```bash
usage: psncli [-h] [--id ID] [--store STORE] [--price PRICE] [--query QUERY] [--json] [--log]

optional arguments:
-h, --help                  show this help message and exit
--id ID, -i ID              CID of game to check
--store STORE, -s STORE     Regional PSN store to check. Default: 'DE/de'
--price PRICE, -p PRICE     Desired price of game
--query QUERY, -q QUERY     Name of item to search for
--json, -j                  Print JSON
--log, -l                   Write to log file
```

#### Retrieving UTF-8 encoded output on terminals

You may have to tell Python that your terminal is capable of dealing with UTF-8 outputs. Some PSN items are annotated with trademark, copyright or foreign language specific symbols. To do so set `export PYTHONIOENCODING=utf-8` in your terminal window.

## Example

You may run this script with the following command line variants:

### Mail alerting - Get a mail when alerts have been met

With `psnmailalert` you may set alerts for price drops in the `alerts.csv` file. The first value is the CID for the item, the second is the price to be matched in order to alert you by mail, and the second value is the store to search in. You may mix stores in the `alerts.csv`. After a price has been matched, the alert is removed from `alerts.csv`. You will not get any further alerts for that item.

```csv
P0001-NPEJ00305_00-B000000000001030,19.00,DE/de
P0001-NPEJ00305_00-B000000000001030,19.00,DE/de
EP0102-CUSA02521_00-MEGAMANLEGACY000,7.00
UP0102-CUSA02516_00-MEGAMANLEGACY000,7.00,US/en
P0101-ULES01372_00-GPCMETALGE000001,10.00,DE/de
```

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

Use the `--json` flag to get the same output as JSON.

```bash
eshopcli --json -q "Dynasty Warriors 8 Xtreme Legends"
[
  {
    "id": "1490013",
    "name": "DYNASTY WARRIORS 8: Xtreme Legends Definitive Edition",
    "type": "GAME",
    "prices": [
      {
        "price": 39.99,
        "currency": "",
        "type": "OFFER"
      }
    ],
    "platforms": [
      "Nintendo Switch"
    ]
  },
...
```

### Check if desired price has been met

The price is in local currency. As exit statuses render the outcome of the alert, you may send mails or desktop notifications with `&&` or `||`. In this example, there is a string printed to the console.

```bash
psncli --id EP0101-ULES01372_00-GPCMETALGE000001 --store DE/de --price 15.00 &&
echo "Price matched, let's buy Metal Gear Solid PW"
```

## Disclaimer

This script is not associated with Sony, Sony PlayStation, the PlayStation Network in any kind. It consumes a public interface that is publicly advertised to the browser to list store contents.

This script is not associated with Nintendo, Nintendo Switch, or the Nintendo Eshop in any kind. It consumes a public interface that is publicly advertised to the browser to list store contents.
