<!-- ![alt text](assets/kasmage_alt.png "Kasmage") -->
<!-- ![alt text](assets/kasmage.png "Kasmage") -->

<table>
<tr>
<td width="160">
  <img src="assets/kasmage.png" width="160" alt="Flubs Ompi, DAG Mage"/>
</td>
<td>
  <h1>Kasmage</h1>
  <p>
    🐸 Kasmage is a whimsical, lightweight frog-wizard themed CLI that monitors a Kaspa address for transactions. It can print all historical transactions or watch for new ones in real time.
  </p>
</td>
</tr>
</table>

> **Fun fact:** <span style="color:#49eacb">**Flubs Ompi, DAG Mage**</span> is the official name of the Kasmage frog.    
> Follow me on X [<span style="color:#db1f83">@evofcl</span>](https://x.com/evofcl) and DM me to suggest cool new epithets!  
> If you're a graphic designer, send me a .png of your frog design — I might just feature it!

##
![PyPI](https://img.shields.io/pypi/v/kasmage) 
![Python](https://img.shields.io/pypi/pyversions/kasmage)

## ⚙️ Quickstart (Install & Run)
<i>Requires Python 3.8+. Tested on 3.10–3.13.</i>

Option 1: Install with pipx (recommended)

pipx installs CLI apps into isolated environments and makes them available globally on your system.

<i>(If you have pipx installed already, skip to step 2)</i>

Step 1.
First, install pipx:
```bash
# if you use homebrew, use:
brew install pipx
pipx ensurepath

# if you don't use homebrew, use:
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# for Windows users (Powershell):
py -m pip install --user pipx
py -m pipx ensurepath
```

⚠️ PATH warning: After installing pipx, you may need to restart your terminal or run
    ```
    exec zsh (or exec bash)
    ```
to refresh your $PATH. If you see zsh: command not found: pipx or zsh: command not found: kasmage, it usually means ~/.local/bin (where pipx puts executables) isn’t in your PATH. Running pipx ensurepath fixes this.

Step 2.
Install Kasmage:
```bash
pipx install kasmage
kasmage --address kaspa:yourkaspaaddresshere

# to upgrade later:
pipx upgrade kasmage
```

Option 2: Install with pip inside a venv
```bash
python -m venv ~/.venvs/kasmage
source ~/.venvs/kasmage/bin/activate
pip install kasmage
kasmage --address kaspa:yourkaspaaddresshere

# to upgrade later:
pip install --upgrade kasmage
```

Option 3: Run from source (for developers). Clone the repo, build the wheel, and install locally:
```bash
git clone https://github.com/yourname/kasmage.git
cd kasmage
poetry build
pip install --force-reinstall dist/kasmage-0.1.0-py3-none-any.whl
```
Now run:
```bash
kasmage --address kaspa:yourkaspaaddresshere
```

## Features

- **Live mode**: watch an address and get notified when new transactions confirm  
- **Historical mode**: print all confirmed transactions (oldest → newest) and exit  
- **Receipts (new!)**: automatically save each detected transaction as a TXT or JSON receipt — useful for bookkeeping, merchants, or your own transaction records.  
- Compatible with Kaspa mainnet addresses (`kaspa:...`)  

## Usage

Watch new transactions (default live mode)
```bash
kasmage --address kaspa:qpwhk9yja6n2l73enwl62s2u52c7u87mjkh4mwhyeueum660ght4735mlsas5
```
Output example:
```bash
🐸🔮 Peering into the orb... (Ctrl+C to stop)
✨👀 I scry with my amphibian eye a tx: 40.00000000 KAS | b7d51e1d29b... | 2025-10-13 07:28:45 UTC
```
Print all past transactions
```bash
kasmage --address kaspa:qpwhk9yja6n2l73enwl62s2u52c7u87mjkh4mwhyeueum660ght4735mlsas5 --historical
```
Output example:
```bash
📜 100.00000000 KAS | txid: 6c7a0b8473b... | 2025-10-12 02:43:09 UTC
📜 200.11837708 KAS | txid: 1a3ede08005... | 2025-10-12 01:21:17 UTC
```

## Options
```
-h, --help          Show this message and exit
-V, --version       Print version and exit
--address           Kaspa address to monitor (required)
--interval          Poll interval in seconds (default: 10)
--page-size         Number of tx per API page (default: 50)
--historical        Print all confirmed tx and exit
--receipts          Write a receipt per new tx (live mode)
--receipts-dir      Directory for receipts (default: ./receipts)
--receipt-format    Receipt format: txt or json (default: txt)
```

## Contributing

I'm new to programming for the crypto space and this might not be anything game-changing but
it's a fun little project to work on. If you have ideas for new features, 
please open a feature request (Issue).  If you’ve built something cool, feel 
free to fork the repo and submit a PR!  

Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/ethanvillalobos8/kasmage/blob/main/LICENSE) © Ethan Villalobos