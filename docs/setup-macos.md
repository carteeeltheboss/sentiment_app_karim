# Run locally on Intel macOS

Use Python 3.11, matching the course. From the repository root:

```bash
uv venv --python 3.11 .venv
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-dev.txt -c constraints-macos-intel.txt
python src/make_demo.py
python src/train.py
python scripts/check_setup.py
pytest -q
```

The demo dataset and trained model are ignored by Git, so they must be recreated
after cloning. Training also updates `models/metrics.json` with the local run date.
The constraints select dependencies with prebuilt Intel Mac wheels. The existing
`requirements.lock` was generated on Windows and includes `pywin32`; use
`requirements.txt` with these constraints here.

Start the API in one terminal, from the repository root:

```bash
source .venv/bin/activate
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Start the interface in another terminal, also from the repository root:

```bash
source .venv/bin/activate
python -m streamlit run ui/app.py --server.address 127.0.0.1 --server.port 8501
```

Open <http://127.0.0.1:8501> for the app or <http://127.0.0.1:8000/docs>
for the API documentation. Stop each server with Ctrl+C.
