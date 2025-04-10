# Future Plans / TODO

## Features planned for next versions

- Automatic `percent_range` calculation based on `price_usd` and `bin_width_usd` to optimally use all available screen rows.
- graceful exit when user presses q, maybe also print out which starting parameters where used.
- Replace `print()` with `curses` for terminal handling and screen refresh.
- Export heatmap snapshot to `.txt` file (and possibly `.png` image export in the future).
- Configurable color schemes for heatmap display.
- When x axis is labeled with blocks, only 4 out of 6 digits are used, solve somehow also the case of blocks with 6+ digits.
- label x axis in available space in lower left corner to show if we are using local time, UTC or blocks (maybe will also solve the above issue).
- Evaluate UTXO filters to reduce noise or crosstalk due to typical 110$-90$ transaction patterns (ATM bias?).
- Handle edge case where two or more blocks are added during the 10-second idle wait (real-time mode).
