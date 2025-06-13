import requests

payload = {
    "memory_blocks": 4,
    "delay": True,
    "memory_type": "global"  # or whatever valid value your backend expects
}

response = requests.post("http://localhost:8000/simulate", json=payload)

if response.status_code == 200:
    print("✅ Simulation triggered successfully!")
else:
    print("❌ Failed to trigger simulation:", response.text)
