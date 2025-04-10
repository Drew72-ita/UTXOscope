# Future Plans / TODO

## Features planned for next versions

- Automatic `percent_range` calculation based on `price_usd` and `bin_width_usd` to optimally use all available screen rows.
- Graceful exit when user presses `q`, maybe also print out which starting parameters were used.
- Replace `print()` with `curses` for terminal handling and screen refresh.
- Export heatmap snapshot to `.txt` file (and possibly `.png` image export in the future).
- Configurable color schemes for heatmap display.
- When the x-axis is labeled with block heights, only 4 out of 6 digits are currently shown — find a way to handle blocks with 6+ digits.
- Label the x-axis in the available space in the lower left corner to indicate whether we are using local time, UTC, or block numbers (this might also solve the previous issue).
- Evaluate UTXO filters to reduce noise or crosstalk due to typical 110$-90$ transaction patterns (ATM bias?).
- Handle the case where two or more blocks are added during the 10-second idle wait (real-time mode).
