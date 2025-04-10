# Future Plans / TODO

## Features planned for next versions

- Automatic `percent_range` calculation based on `price_usd` and `bin_width_usd` to optimally use all available screen rows.
- Replace `print()` with `curses` for terminal handling and screen refresh.
- Export heatmap snapshot to `.txt` file (and possibly `.png` image export in the future).
- Configurable color schemes for heatmap display.
- Evaluate UTXO filters to reduce noise or crosstalk due to typical 110$-90$ transaction patterns (ATM bias?).
- Handle edge case where two or more blocks are added during the 10-second idle wait (real-time mode).
