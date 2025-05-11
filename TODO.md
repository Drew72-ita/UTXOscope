# Future Plans / TODO

## Features planned for next versions

- Graceful exit when user presses `q`, maybe also print out which starting parameters were used.
- manage a moving buffer of UTXO amounts in memory (since we are using moving average of last N blocks)
- Replace `print()` with `curses` for terminal handling and screen refresh.
- Export heatmap snapshot to `.txt` file [done] (and possibly `.png` image export in the future).
- recoding of frames in some format for later playback [done]
- Optional color scheme for heatmap display, differentiating UTXO type (data, single TX with change, all the others)
- When the x-axis is labeled with block heights, only 4 out of 6 digits are currently shown — find a way to handle blocks with 6+ digits.
- Label the x-axis in the available space in the lower left corner to indicate whether we are using local time, UTC, or block numbers (this might also solve the previous issue).
- Toggle the x-axis labels, and perhaps add a fourth label type that displays the number of transactions used to construct a specific heatmap column.
- Toggle y-axis label to display bins in ksatoshis (corresponding to \$100, \$50 or \$200).
- Handle the case where two or more blocks are added during the 10-second idle wait (real-time mode).
