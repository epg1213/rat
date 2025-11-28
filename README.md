
# RAT

Malware that executes remote commands via an encrypted socket

![poc](poc.png?raw=true)

## Installation

```bash
git clone https://github.com/epg1213/rat
cd rat
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run (server - side)

```bash
python server.py SERVER_IP_ADDRESS
```

## Run (client - side)

```bash
python client.py SERVER_IP_ADDRESS
```

