# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- ## [Unreleased]
### Added

### Changed -->


---

## [0.4.0] - 2025-10-16
### Added
- **Threshold filtering**: new `--threshold` flag to only show transactions where the absolute amount is greater than or equal to the specified KAS value.
- **Direction filtering**: new `--dir` flag to show only `in` or `out` transactions.  
  Useful for miners (filtering only payouts) or merchants (filtering only incoming payments).

### Changed
- Live mode now respects threshold and direction filters before printing or writing receipts.

---

## [0.3.0] - 2025-10-15
### Added
- Historical mode output styles:
  - `--historical-style` (`table`, `ledger`, or `jsonl`)
  - `--historical-tz` (IANA tz like `America/Chicago`, or `local` for system timezone)
  - `--historical-limit` to cap rows
  - `--historical-newest-first` for reverse ordering
  - `--short-txid` flag to toggle between shortened or full txids
  - `--no-color` flag to disable ANSI coloring
- `--receipts-dir-style` option for per-address folder naming (`short` = first 10 chars, `full` = full address)
- Local time support for historical output and receipts

### Changed
- Improved table formatting for historical mode (aligned columns, optional borders)
- Receipts now include ISO timestamps (`issued_utc_iso`, `time_utc_iso`)
- More robust API fetch with retries, backoff, and user-agent header

### Fixed
- Consistent handling of invalid addresses with clear warning messages
- Better filename sanitization across platforms for receipts and directories

---

## [0.2.0] - 2025-10-13
### Added
- `--receipts` flag to write a receipt per new transaction in live mode
- `--receipts-dir` (default: `receipts/`)
- `--receipt-format` (`txt` or `json`)