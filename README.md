# UTXOscope
UTXOscope is a text-only BTC blockchain analysis tool that visualizes price dynamics using only on-chain data.
Unlike traditional methods that rely on external exchanges or price feeds, UTXOscope estimates the Bitcoin price trend by analyzing the value distribution of newly created UTXOs (Unspent Transaction Outputs) directly from the blockchain.

The general idea is inspired by UTXOracle by Simple Steve (see https://utxo.live/oracle/). 

The  project runs fully locally using your own Bitcoin Core node and bitcoin-cli.

![quicklook](images/fig01a.gif)

<small><i>Eye-catching animated GIF, move along (accelerated run made with v.0.4.2)</i></small>


## Core Idea

The fundamental assumption behind **UTXOscope** is that the most common transaction size for retail users is a round-number fiat purchase — typically **$100**.

By analyzing the frequency and distribution of UTXOs corresponding to typical purchase amounts (**$100**, **$50**, and **$200**), it becomes possible to infer historical price trends and track their movement over time.

Some UTXOs are excluded from the analysis:
- UTXOs with `nulldata` or `nonstandard` output types (typically associated with inscriptions, runes, or other metadata).
- UTXOs divisible by **1,000 sats** (e.g., 100,000 sats, 1,000 sats, 75,000 sats, 29,000 sats), as they appear far more frequently than expected due to human bias toward round numbers. Statistically, such outputs should represent only about 0.1% of all cases.  
  This effect is particularly visible around the **$100,000** price level, where **$100 = 100,000 sats**.

## Features
- No external price feed — fully self-contained analysis using blockchain data.
- ASCII-based heatmap visualization directly in the terminal.
- Real-time update as new blocks are mined, can start N blocks in the past to fill the screen.
- Configurable price range and binning for different display resolutions.
- Optional x-axis labeling of timestamps in: Local time, UTC, or the current block height (last 4 digits).
- Automatic (beta) tracking of price when price movements exceed the displayed range.

## Basic usage
The tool connects to a local Bitcoin Core full node and scans recent blocks to build a heatmap of UTXO creation sizes.

The script works with the user able to run `bitcoin-cli` (try to launch: `bitcoin-cli getblockcount` ), no other prerequisites.

`python3 UTXOscope.py`

Six parameters will be asked to the user, prompts should be self-explanatory.

Default parameters (hit enter at every request) are tuned for visualizing a price range around \$95,000 ± 3% on a standard 80x24 terminal window, starting from 70 blocks in the past to fill the screen. If you are using standard parameters, check that the first is at least compatible with current price, so with BTC real price of \$100.000 standard parameters will not work, try 100.000 ± 3%.

If too few lines are available on the terminal, the program will progressively reduce the percent range. 

Alternatively, it is possible to explore historical price dynamics by specifying a starting block and custom parameters.

## Usage Tips

To reduce the impact on system performance, you may want to run the Python script with lower priority:

`nice -n 19 python3 UTXOscope.py`

For longer runs, especially when connected to the node via SSH, consider running the script inside a `tmux` session. This allows the script to continue running even if the SSH connection is interrupted. You can later reattach to the session.


## Log / Replay Feature (from v0.4.2)

Running the script with `log` as a command-line argument:

`python3 UTXOscope.py log`

will create a log file named `log_timestamp.txt` (timestamp=`%y%m%d%H%M%S`) , which records all rendered frames in plain text.

This allows you to "run and forget" the script inside a `tmux` session, and monitor its output with a simple `tail -f` on the log file.

You can later replay the log by providing the filename, a delay in milliseconds between frames, and an optional starting block:

`python UTXOreplay.py <logfile.txt> <delay_ms> [start_block]`

**Example:**

`python UTXOreplay.py log_250421134024.txt 100 893300`

The block number is optional but must be present in the log.


## Examples
To explore price activity on a 80x24 terminal starting from April 2nd, 2025:

`python3 UTXOscope.py` 

Entering the six parameters (requested on five separate prompts at startup):

`84000 5 500 3 890504 B`

[![YouTube 30s demo](https://img.youtube.com/vi/meTtSqal6y8/hqdefault.jpg)](https://youtu.be/meTtSqal6y8)

*(YouTube 30 sec demo with above parameters, click to play)*

This will process about one day of data in 15 minutes on bitcoin core setups like Raspibolt

(fig. 01 for a "cloudy" day, fig 02  for clearer skyes)

![Example of output running on a Raspibolt + output on a 7' HDMI LCD](images/fig01b.jpg)

**Fig.01:** *Example of output running on a Raspibolt + output on a 7' HDMI LCD (100x30 chars). In this example, the weaker trend line above the main signal is probably coming from sales of OC sats for \$100, including 7-8% total fees (seller+service+miner), thus buying less sats for the buck and projecting a 7-8% higher BTC price. Vertical lines correspond with odd blocks containing mostly data/payload transactions (made with v.0.4.0). Update: this singnal 7-8% price + fee signal should be less visible from v.0.4.1 *

![Example of output running on a Raspibolt + output on a 7' HDMI LCD](images/fig02.jpg)

**Fig.02:** *90 blocks later, a sharper and cleaner profile: it depends on the day and the type of transactions / UTXOs (made with v.0.4.0).*

![Example of output running on a Raspibolt + output on a 7' HDMI LCD](images/fig03.jpg)

**Fig.03:** *The most informative y-axis resolution is 250$ dollars (third parameter), this example was launched on a 7' HDMI LCD (100x30 chars), but the tracking could get lost if the price changes more than +/-3% in 2-3 blocks. In this case the x axis is labeled with local time in hours. (made with v.0.4.0).*

![Example of output running on a Raspibolt + output on a 7' HDMI LCD](images/fig04.jpg)

**Fig.04:** *Similar to fig.03, but some time later and with a clearer signal (made with v.0.4.1 using signal lower/higher harmonics from \$200 and \$50 purchases).*

![Testing different price resolutions on a 100x30 tmux session](images/fig05.jpg)

**Fig.05:** *Testing different price range resolutions: higher res are more informative, but probably the auto-tracking logic will fail more easily in case of rapid price change (made with v.0.4.1.* on a raspibolt, three tmux sessions on 100x30 chars terminals)


## Requirements
- Bitcoin Core full node with RPC access (bitcoin-cli).
- Python 3.x.

## Tips / buy me a coffee ^_^
**Bolt12 LN** 

lno1zrxq8pjw7qjlm68mtp7e3yvxee4y5xrgjhhyf2fxhlphpckrvevh50u0q29vqjjqgyu80agddjw9xwup56yka8t9hzq8audxmks66zepgqga7qsr9jmvaqlf7efa89v8tjvn5tcsfvxmz5cspdjglqv93lw97e8je6dsqvljglw2m5jg0tsmxwjj2mwgp7aprm5k5xuttf5pwxghh0qtrx28g8lqmq7yd28ysp9k7x4x5j4r8wqaa6sjqwwx3m68mszkfruas09hwpm23t4yr9pevaqa8022ps705p9jtndawqqsp8h4gukup8ejnsz7fcwr6tn8y5

<img src="images/bolt12.jpeg" alt="Bolt 12 QR code" width="200">

**Wallet of Satoshi** : drew (at) walletofsatoshi.com


## Disclaimer
This is an experimental tool and a very preliminary release.

It will fail if Bitcoin Core stops or if unexpected parameters are entered by the user.

Nothing harmful should happen in any case, this is just a python script calling bitcoin-cli locally and doing some calculations.
