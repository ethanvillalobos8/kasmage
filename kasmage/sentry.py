import argparse
import os
import re
import time
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

import requests

"""
As of 2025-10, the Kaspa REST-API does not support testnet addresses.
When it does, we can use the regex below.

Kaspa REST API docs and examples (note camelCase response keys):
- https://api.kaspa.org/docs#/
- https://docs.kas.fyi/api-reference/v1/address/get-address-transactions
"""

# -------- Settings --------
ADDRESS_RX = re.compile(r"^kaspa:[a-z0-9]{61,63}$")  # mainnet only
PAGE_SIZE = 50

# -------- API --------
def fetch_transactions_page(address: str, *, limit=PAGE_SIZE, offset=0) -> List[Dict[str, Any]]:
    """
    Returns a list of tx dicts from /addresses/{address}/full-transactions.
    Uses snake_case per your sample payload.
    """
    url = f"https://api.kaspa.org/addresses/{address}/full-transactions"
    headers = {"accept": "application/json"}
    params = {
        "limit": limit,
        "offset": offset,
        "resolve_previous_outpoints": "full",  # needed to attribute inputs
    }
    r = requests.get(url, headers=headers, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("transactions") or data.get("items") or []
    return []

def fetch_all_transactions(address: str, *, page_size=PAGE_SIZE, max_pages=200) -> List[Dict[str, Any]]:
    all_txs: List[Dict[str, Any]] = []
    offset = 0
    for _ in range(max_pages):
        page = fetch_transactions_page(address, limit=page_size, offset=offset) or []
        if not page:
            break
        all_txs.extend(page)
        if len(page) < page_size:
            break
        offset += page_size
    return all_txs

# -------- Parsers --------
def parse_tx_id(tx: Dict[str, Any]) -> str:
    return str(tx.get("transaction_id") or tx.get("hash") or "unknown")

def parse_time(tx: Dict[str, Any]) -> Optional[int]:
    """Return block_time in ms if present, else None."""
    t = tx.get("block_time") or tx.get("timestamp")
    try:
        t = int(t)
        return t if t >= 10**12 else t * 1000  # normalize to ms
    except Exception:
        return None

def format_time_ms(t_ms: Optional[int]) -> str:
    if t_ms is None:
        return "no-time"
    dt = datetime.fromtimestamp(t_ms/1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")

def norm(s: Optional[str]) -> str:
    return s.lower() if isinstance(s, str) else ""

def net_amount_kas_for_address(tx: Dict[str, Any], address: str) -> float:
    """
    Compute (sum outputs to address) - (sum inputs from address), in KAS.
    Uses ONLY snake_case keys from the sample payload.
    """
    addr = norm(address)

    out_total = 0
    for o in tx.get("outputs") or []:
        o_addr = norm(o.get("script_public_key_address") or o.get("address"))
        if o_addr == addr:
            try:
                out_total += int(o.get("amount", 0))
            except Exception:
                pass

    in_total = 0
    for i in tx.get("inputs") or []:
        i_addr = norm(i.get("previous_outpoint_address") or i.get("address"))
        val = i.get("previous_outpoint_amount") or i.get("value")
        if i_addr == addr and val is not None:
            try:
                in_total += int(val)
            except Exception:
                pass

    return (out_total - in_total) / 1e8  # sompi -> KAS

# -------- Modes --------
def run_historical(address: str, page_size: int):
    """Print ALL historical transactions (oldest→newest) and exit."""
    txs = fetch_all_transactions(address, page_size=page_size)
    if not txs:
        print("📜 No transactions found.")
        return 0
    # Oldest → newest for readability
    txs.sort(key=lambda tx: parse_time(tx) or 0)
    for tx in txs:
        txid = parse_tx_id(tx)
        amt = net_amount_kas_for_address(tx, address)
        t_ms = parse_time(tx)
        print(f"📜 {amt:.8f} KAS | txid: {txid} | {format_time_ms(t_ms)}")
    return 0

def run_live(address: str, interval: int, page_size: int):
    """
    Live mode:
      - Seed 'seen' with ALL txids currently on-chain for this address (so we only
        announce current/future ones).
      - Then poll and print any new tx once.
    """
    if not ADDRESS_RX.match(address):
        print(f"Invalid address: {address}")
        return 1

    # Seed seen with ALL current txids (so we don't announce history)
    current = fetch_all_transactions(address, page_size=page_size)
    seen = {parse_tx_id(tx) for tx in current if parse_tx_id(tx)}

    print("🐸🔮 Peering into the orb... (Ctrl+C to stop)")
    try:
        while True:
            # Poll newest pages; first page is enough for most usage,
            # but we’ll do a short walk just in case multiple txs land quickly.
            offset = 0
            while True:
                page = fetch_transactions_page(address, limit=page_size, offset=offset) or []
                if not page:
                    break
                for tx in page:
                    txid = parse_tx_id(tx)
                    if not txid or txid in seen:
                        continue
                    seen.add(txid)
                    amt = net_amount_kas_for_address(tx, address)
                    t_ms = parse_time(tx)
                    print(f"✨👀 I scry with my amphibian eye a tx: {amt:.8f} KAS | {txid} | {format_time_ms(t_ms)}")
                if len(page) < page_size:
                    break
                offset += page_size

            time.sleep(max(1, interval))
    except KeyboardInterrupt:
        print("\n💫 Spell countered.")
        return 0
    

# -------- Art --------
FROG_KASMAGE = r"""
                        
                     .@@@.                       
                    @*=-@#                       
                   @  ==%@                       
                  %+===+*%@                      
                 @#= -=+##@.                    
               :#+=+.=++=*%@                    
            =%%@@+++.=*+ :%@          ] .  m,  m, .mm  m,  mm  m, 
           @@#==+****@@@@@@@@@@@      ].` ' ] ] ' ]]] ' ] ]`T ]`] 
             %.@@@@@@@@@@@%%%@@@      ]T  ."T  "\ ]]] ."T ] ] ]"" 
            .+*+.    =@@# %-          ] \ 'mT 'm/ ]]] 'mT 'bT 'b/ 
            %*----------   -+                              ,]
             +               -%                            '`
              @             %%=@:               
            %:%       %   @     @@              
            -*@ #     % = @      @              
           +%*@ *@    % @=:+%*  @:              
          %@@=%@ .%@@.# @@ .  %@=               
                            ...                     
"""

# -------- CLI --------
def main():
    print(FROG_KASMAGE)
    p = argparse.ArgumentParser(description="Kaspa tx logger (historical or live)")
    p.add_argument("--address", required=True, help="kaspa:...")
    p.add_argument("--interval", type=int, default=10, help="poll seconds (live mode)")
    p.add_argument("--page-size", type=int, default=PAGE_SIZE, help="transactions per page")
    p.add_argument("--historical", action="store_true",
                   help="print ALL historical transactions once, then exit")
    args = p.parse_args()

    if args.historical:
        return run_historical(args.address, page_size=args.page_size) or 0
    else:
        return run_live(args.address, interval=args.interval, page_size=args.page_size) or 0

if __name__ == "__main__":
    raise SystemExit(main())