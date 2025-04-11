# UTXOscope
UTXOscope is a text-only BTC blockchain analysis tool that visualizes price dynamics using only on-chain data.
Unlike traditional methods that rely on external exchanges or price feeds, UTXOscope estimates the Bitcoin price trend by analyzing the value distribution of newly created UTXOs (Unspent Transaction Outputs) directly from the blockchain.

The general idea is inspired by UTXOracle by Simple Steve (see https://utxo.live/oracle/). 

The  project runs fully locally using your own Bitcoin Core node and bitcoin-cli.

## Core Idea
The fundamental assumption behind UTXOscope is that the most common transaction size for retail users is a round-number fiat purchase — typically $100.
By analyzing the frequency and distribution of UTXOs that correspond to typical purchase amounts (at the moment only $100 worth of Bitcoin), it becomes possible to infer the historical price trend and track its movements over time.

## Features
- No external price feed — fully self-contained analysis using blockchain data.
- ASCII-based heatmap visualization directly in the terminal.
- Real-time update as new blocks are mined.
- Configurable price range and binning for different display resolutions.
- Optional display of timestamps in Local time, UTC, or the current block height.
- Automatic (beta) tracking of price when price movements exceed the displayed range.

## Usage
The tool connects to a local Bitcoin Core full node (bitcoin-cli) and scans recent blocks to build a heatmap of UTXO creation sizes.

python3 UTXOscope.py

Default parameters (hit enter at every request) are tuned for visualizing a price range around $80,000 ± 6% on a standard 80x24 terminal window.
Alternatively, it is possible to explore historical price dynamics by specifying a starting block and custom parameters.

## Example
To explore price activity starting from April 2nd, 2025:

python3 UTXOscope.py 

Entering the five parameters (requested on five separate prompt at startup):

84000 5 500 3 89504 B

[![Watch the video](https://img.youtube.com/vi/meTtSqal6y8/hqdefault.jpg)](https://youtu.be/meTtSqal6y8)

This will process about one day of data in 15 minutes on a low-powered device like a Raspibolt.

## Requirements
- Bitcoin Core full node with RPC access (bitcoin-cli).
- Python 3.x.

## Disclaimer
This is an experimental tool and a very preliminary release.

It will fail if Bitcoin Core stops or if unexpected parameters are entered by the user.

Nothing harmful should happen in any case, this is just a python script calling bitcoin-cli locally and doing some calculations.

