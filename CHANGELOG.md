# Changelog

## [0.4.2.0] - 2025-05-02

- Added **log** (`UTXOscope.py`) and **replay** (`UTXOreplay.py`) functionality.
- Introduced a startup splash screen with script name and version.
- Excluded 0.1% of UTXOs with amounts divisible by 1,000 sats (to reduce human rounding bias).
- Improved Y-axis price label alignment (supports values from ` 10,000$` to `999,999$`).
- Optimized bin-filling loops for better performance.
- Added input constraints to key parameters (range and validation).
- Changed default parameters to: `95000`, `3`, `250`, `3`, `70`, `B`.

## [0.4.1.2] - 2025-04-26
- Update to README.md + moving images in images folder, no change to python code
- This is a cleanup in preparation for upcoming 0.4.2 release

## [0.4.1.1] - 2025-04-16
- small fix to tracking logic tresholds

## [0.4.1.0] - 2025-04-16
### Added
- Automatic reduction of `percent_range` if not enough screen rows are available.
- Added signal from $50 and $200 purchases to reduce backround noise and enhance signal
- Standard parameters are now 84000 3 250 3 70 L

## [0.4.0] - 2025-04-10
- Initial public release on GitHub
