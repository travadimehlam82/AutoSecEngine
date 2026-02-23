# AutoSecEngine — Autonomous Endpoint Security Monitoring Engine (Option B)

## Summary
AutoSecEngine is a full-featured endpoint security demo project for academic submission. It includes:
- Safe ransomware behavior simulator (operates only inside a configurable test folder and makes backups)
- File-system monitor using Watchdog
- Entropy-based feature extraction + AES-based safe simulation (operates on copies)
- A lightweight ML anomaly detector (RandomForest) trained on synthetic features to demonstrate classification
- Flask web dashboard showing live events and detection results

**Important:** This project is educational. Do NOT point the test folder to real personal documents. Use a dedicated test directory.

## Quickstart (VS Code)
1. Open this folder in VS Code.
2. Create & activate virtual environment:
   - Linux/macOS:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows PowerShell:
     ```
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a safe test folder (default: `~/autosec-test`) and add some `.txt` files.
   - Linux/macOS: `mkdir ~/autosec-test && echo "hello" > ~/autosec-test/sample1.txt`
   - Windows PowerShell: `mkdir $env:USERPROFILE\autosec-test; "hello" | Out-File $env:USERPROFILE\autosec-test\sample1.txt`
5. Run components in separate terminals:
   - `python monitor.py`            # starts detector/monitor
   - `python app.py`                # starts Flask dashboard (http://127.0.0.1:5001)
   - `python simulator.py`          # runs safe simulator (creates backups and modifies only test folder)
6. Optional: Train or evaluate ML detector:
   - `python ml_detector.py --train`   # trains a small RandomForest on synthetic data and saves model

## Folder layout
- monitor.py           : watcher + detector logic
- simulator.py         : safe behavior simulator
- encryption.py        : AES helper (used safely on copies)
- ml_detector.py       : simple RandomForest demo (synthetic)
- app.py               : Flask dashboard + API
- templates/           : dashboard HTML template
- static/              : (empty) for CSS/JS if needed
- requirements.txt

## Safety notes
- The simulator creates backups in the project folder before modifying files.
- Quarantine folder and backups are created inside the project root; real user files are never targeted.
