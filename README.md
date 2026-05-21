# MiniMax Useful Tools

## Simple Proxy for Github Copilot in VS Code

### Setup

```bash
# Set your API key as env variable
export MINIMAX_API_KEY="your-key-here"
```

### Run proxy

```bash
# python
python minimax_proxy.py

# python with verbose output
python minimax_proxy.py --verbose

# javascript as fallback if trouble with python
node minimax_proxy.js
```

### Github Copilot in VS Code
In Copilot sidebar click on Model -> Manage Language Models -> Open Language Models (JSON)

See `chatLanguageModels.json.example` for setting up custom endpoints.

### Troubleshoot
Test endpoint and auth key inject working:
```bash
curl -X POST http://localhost:3333/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2.7","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
```

### Run as service
Example how to install as systemd user service on startup.

```bash
sudo mkdir -p /opt/minimax-useful-copilot
sudo chown -R $USER: /opt/minimax-useful-copilot
git clone https://github.com/AlmightyFrog/minimax-useful-copilot /opt/minimax-useful-copilot
cd /opt/minimax-useful-copilot

mkdir -p ~/.config/systemd/user/

echo "MINIMAX_API_KEY=$MINIMAX_API_KEY" > ~/.config/minimax-api-key
chmod 600 ~/.config/minimax-api-key

cp minimax-proxy.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable minimax-proxy

systemctl --user start minimax-proxy
```
