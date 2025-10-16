# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- ## [Unreleased]
### Added
### Changed
### Fixed
-->

---

## [0.5.0] - 2025-10-16
### Added
- **Verification (live)**: `--verify AMOUNT` (repeatable) flags exact **inbound** payments that match the specified amount.  
  - Multiple amounts are supported (e.g., `--verify 1 --verify 1 --verify 5.25`).
  - Each amount is only verified once per occurrence (no re-flagging).
- **Threshold filtering (live)**: `--threshold KAS` shows only **inbound** transactions whose amount is `>=` the threshold.  
  - Plays alert sound when combined with `--alert`.
- **Direction filtering (both modes)**: `--dir {in,out}` to restrict displayed tx by direction.
- **Alert sounds (live)**: `--alert` plays a sound for **verify hits** and **threshold hits** (optional, off by default).
- **Sender display**: live logs now show a compact list of input (sender) addresses under each printed transaction or verification line.
- **Version notifications**: Kasmage now checks PyPI on startup and prints a friendly message:  
  - If you’re on the **latest version**, it confirms you’re up to date.  
  - If you’re on an **older version**, it suggests upgrade commands.  
  - If you’re on a **dev build newer than PyPI**, it notes that too.

### Changed
- Historical mode now blocks incompatible live-only flags (`--verify`, `--threshold`, `--receipts`, etc.) with a clear error message.
- Threshold and verification logging bypass normal filters (ensuring they always display once triggered).
### Changed
- **Historical guardrails**: when `--historical` is used, live-only flags are rejected (`--receipts`, `--receipts-dir*`, `--receipt-format`, `--min-amount`, `--threshold`, `--verify`, `--alert`).
- **Threshold vs direction**: `--threshold` is inbound-only and **cannot** be combined with `--dir`. If you need direction filtering without threshold, use `--dir` alone.
- **No double-logging**: when a transaction triggers a verification, only the verification line is printed (and one receipt, if enabled). The same tx will not also be printed as a “normal” live log.

### Fixed
- More robust, quiet handling of update checks and optional sound playback errors (no crashes on network/audio issues).
- Cleaner handling of invalid/unsupported combinations of flags, with clear error messages.

### Packaging
- **WAV asset** for alerts is now included in the wheel/sdist and resolved at runtime via `importlib.resources` (zip-safe).
- `playsound` is **optional**; alerts only play if `--alert` is set and `playsound` is installed.

---

## [0.4.0] - 2025-10-16
### Added
- **Threshold filtering**: new --threshold flag to only show transactions where the absolute amount is greater than or equal to the specified KAS value.
- **Direction filtering**: new --dir flag to show only in or out transactions.  
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