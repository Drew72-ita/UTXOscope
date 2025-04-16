# ======================================================================
# UTXOscope - general idea from UTXOracle
# (see https://utxo.live/oracle/)
# Author: Drew72-ita
# Version: 0.411-RC1
# ======================================================================
# This is a very preliminary release.
# Will run on a Bitcoin Core installation using bitcoin-cli.
# It will fail with unexpected parameters or if Bitcoin core stops.
#
# You have to provide a price range.
# Standard parameters are ok for current price 80.000$ +/- 6%.
# on a standard 80x24 console screen: it will fill the graph with last
# 70 blocks and go into realtime, checking for new blocks every 10s.
#
# Or you can try the price dynamics from 2nd Apr 2025 with:
# 84000,5,500,3,89504,B     ( see https://youtu.be/meTtSqal6y8 )
# It will process one day of data in 15 mins on a raspibolt.
# ======================================================================

import subprocess
import json
import math
import time
import shutil
import os
import sys
from datetime import datetime, timezone

cols, rows = shutil.get_terminal_size()
cols -= 1  # force one-column margin to avoid overflow

# === BEGIN Prompt user for starting parameters ===
try:
    price_usd = float(input("Indicative BTC/USD price [default 84000]: ") or "84000")
    percent_range = float(input("+/- range to explore as percentage [default 3 for 80x24 std console]: ") or "3")
    bin_width_usd = float(input("Bin width in $ [default 250 - usually best results]: ") or "250")
    block_count = int(input("Number of consecutive blocks to analize [default 3 and should stay 3]: ") or "3")
    start_offset = int(input("Start from N blocks ago (≤1000) or block height (>1000) [default 70]: ") or "70")
    if start_offset <= 0:
        start_offset = 1
    tz_choice = input("Timestamp in (L)ocal, (U)TC or  (B)lock number? [default L]: ").strip().lower()
    use_utc = False
    use_block_number = False
    if tz_choice.startswith('u'):
        use_utc = True
    elif tz_choice.startswith('b'):
        use_block_number = True

except ValueError:
    print("Invalid input. Exiting.")
    exit(1)
# === END Prompt user for starting parameters ===

# === BEGIN perform initial one-time only calculations with provided parameters ===
usd_purchase = 100
reserved_rows = 5
move_graph = 0

while True: # some calcs. and progr. reduction of percent_range if there are to few rows in the terminal
    raw_min_price = price_usd * (1 - percent_range / 100)
    raw_max_price = price_usd * (1 + percent_range / 100)
    min_price = math.floor(raw_min_price / bin_width_usd) * bin_width_usd
    max_price = math.floor(raw_max_price / bin_width_usd) * bin_width_usd
    price_bins = list(range(int(min_price), int(max_price) + 1, int(bin_width_usd)))
    satoshi_bins = [int((usd_purchase * 100_000_000) / p) for p in price_bins]
    price_bins = price_bins[:-1]
    satoshi_bins = satoshi_bins[:-1]
    grid_height = len(satoshi_bins) - 1
    smoothed_median_bin = grid_height // 2  #initialize smoothed_median_bin at the middle value
    usable_rows = rows - reserved_rows
    if usable_rows >= grid_height:
        break
    print(f"Too few rows available, reducing percent_range to {percent_range - 0.1:.1f}")
    time.sleep(0.25)
    percent_range -= 0.1

graph_cols = cols - 7
ascii_grid = [[" " for _ in range(graph_cols)] for _ in range(grid_height)]
x_labels = ["    " for _ in range(graph_cols)]
col_index = 0
# === END perform initial one-time only calculations with provided parameters ===

# === BEGIN function definitions ===
def bitcoin_cli(*args):
    cmd = ['bitcoin-cli'] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def ascii_bar(percent):
    if   percent >= 97: return '█'  # the percent thresholds
    elif percent >= 75: return '▓'  # are only relevant for a nice
    elif percent >= 53: return '▒'  # brightness/contrast of the
    elif percent >= 31: return '░'  # heatmap, all in all they work as
    elif percent >= 10: return '·'  # brightnesss/contrast adjustments
    else: return ' '

def get_bin_counts(block_hash):
    bin_counts = [0] * grid_height
    current_hash = block_hash
    for _ in range(block_count):
        block = json.loads(bitcoin_cli("getblock", current_hash, "2"))
        for tx in block['tx']:
            for vout in tx['vout']:
                spk_type = vout.get('scriptPubKey', {}).get('type', '')
                if spk_type in ['nulldata', 'nonstandard']:
                    continue
                sats = int(vout['value'] * 1e8)         #<--- case of $ 100 purchases (main signal)
                for i in range(grid_height):
                    if satoshi_bins[i+1] <= sats < satoshi_bins[i]:
                        bin_counts[i] += 1
                        break
                sats = int(vout['value'] * 1e8 * 2)     #<--- case of $ 50 purchases (lower harmonic)
                for i in range(grid_height):
                    if satoshi_bins[i+1] <= sats < satoshi_bins[i]:
                        bin_counts[i] += 1
                        break
                sats = int(vout['value'] * 1e8 // 2)    #<--- case of $ 200 purchases (higher harmonic)
                for i in range(grid_height):
                    if satoshi_bins[i+1] <= sats < satoshi_bins[i]:
                        bin_counts[i] += 1
                        break
        if 'previousblockhash' in block:
            current_hash = block['previousblockhash']
        else:
            break
    return bin_counts

def render_ascii_graph():
    os.system("clear")

    # Calculate median bin as weighted average of map
    weights = []
    for r in range(grid_height):
        char = ascii_grid[r][col_index - 1]
        if char == '█': w = 1.0    # weights are relevant
        elif char == '▓': w = 0.75 # to tweak median bin calc
        elif char == '▒': w = 0.5  
        elif char == '░': w = 0.1
        else: w = 0.0  
        weights.append(w)

    total_weight = sum(weights)
    if total_weight < 0.1:
        median_bin = grid_height // 2
    else:
        weighted_sum = sum(w * i for i, w in enumerate(weights))
        median_bin = int(round(weighted_sum / total_weight))

    global last_median_bin
    global smoothed_median_bin
    global move_graph
    smoothed_median_bin = 0.65 * smoothed_median_bin + 0.35 *  median_bin 
    median_bin = int(round(smoothed_median_bin))
    last_median_bin = median_bin  

    # Decide if it is necessary to move graph up/down to track price
    threshold = grid_height // 3  
    if median_bin < threshold:
        move_graph = -1
    elif median_bin >= grid_height - threshold:
        move_graph = 1
    else:
        move_graph = 0

    # Select median bin marker according to next graph movement
    if move_graph == 1:
        direction_char = "↑"
    elif move_graph == -1:
        direction_char = "↓"
    else:
        direction_char = ">"

    # y axis label with dollar or median bin marker
    for r in reversed(range(grid_height)):
        arrow_or_dollar = direction_char if r == median_bin else "$"
        label = f"{price_bins[r]:5d}{arrow_or_dollar} "  # <- a space is added at the end
        print(label + "".join(ascii_grid[r]))

    # x axis
    for i in range(4):
        print("       ", end="")
        for c in range(graph_cols):
            print(x_labels[c][i] if i < len(x_labels[c]) else " ", end="")
        print()
# === END function definitions ===

# === BEGIN one-time only part that needs functions ===
current_height = int(bitcoin_cli("getblockcount"))
if start_offset > 1000:
    target_height = start_offset
else:
    target_height = current_height - start_offset + 1
last_block = bitcoin_cli("getblockhash", str(target_height))
# === END one-time only part that needs functions ===

# === BEGIN Main loop ===
while True:
    bin_counts = get_bin_counts(last_block)
    max_count = max(bin_counts) if any(bin_counts) else 1
    column = [ascii_bar((c / max_count) * 100) for c in bin_counts]

    blockinfo = json.loads(bitcoin_cli("getblock", last_block))
    dt = datetime.fromtimestamp(blockinfo["time"])
    if use_utc:
        dt = dt.astimezone(timezone.utc)
    if use_block_number:
        block_height = blockinfo["height"]
        time_label = str(block_height)[-4:].rjust(4)
    elif use_utc:
        time_label = datetime.utcfromtimestamp(blockinfo["time"]).strftime("%H%M")
    else:
        time_label = datetime.fromtimestamp(blockinfo["time"]).strftime("%H%M")

    if col_index < graph_cols:
        for r in range(grid_height):
            ascii_grid[r][col_index] = column[r]
        x_labels[col_index] = time_label.ljust(4)
        col_index += 1
    else:
        for r in range(grid_height):
            ascii_grid[r] = ascii_grid[r][1:] + [column[r]]
        x_labels.pop(0)
        x_labels.append(time_label.ljust(4))

    render_ascii_graph()

    if move_graph != 0:
        shift_bins = (grid_height // 4) * move_graph # this is very relevant: shift 1/4 (not 1/3) of the screen
        shift = abs(shift_bins)

        # update price range
        min_price += shift_bins * bin_width_usd
        max_price += shift_bins * bin_width_usd

        # recalc binning
        price_bins = list(range(int(min_price), int(max_price) + 1, int(bin_width_usd)))
        satoshi_bins = [int((usd_purchase * 100_000_000) / p) for p in price_bins]
        price_bins = price_bins[:-1]
        satoshi_bins = satoshi_bins[:-1]

        # shift graph up or down
        if move_graph == 1:
            new_grid = ascii_grid[shift:]
            ascii_grid = new_grid + [[" " for _ in range(graph_cols)] for _ in range(grid_height - len(new_grid))]
        elif move_graph == -1:
            new_grid = ascii_grid[:-shift]
            ascii_grid = [[" " for _ in range(graph_cols)] for _ in range(grid_height - len(new_grid))] + new_grid
        
        smoothed_median_bin -= move_graph * shift
        move_graph = 0  # reset for next cycle

    if 'nextblockhash' in blockinfo:
        last_block = blockinfo['nextblockhash']
    else:
        while True:
            time.sleep(10)
            new_block = bitcoin_cli("getbestblockhash")
            if new_block != last_block:
                last_block = new_block
                break
# === END Main loop ===
