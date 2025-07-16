import requests
import json
import time

RPC_URL = "https://rpc.ankr.com/eth"  # или любой другой публичный RPC

def get_latest_block_number():
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    response = requests.post(RPC_URL, json=payload).json()
    return int(response["result"], 16)

def get_block_by_number(block_number):
    hex_block = hex(block_number)
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex_block, False],
        "id": 1
    }
    response = requests.post(RPC_URL, json=payload).json()
    return response["result"]

def mirror_blocks(n=10):
    latest = get_latest_block_number()
    mirrored = []

    for i in range(n):
        block_num = latest - i
        block = get_block_by_number(block_num)
        if block:
            mirrored.append({
                "number": int(block["number"], 16),
                "hash": block["hash"],
                "miner": block["miner"],
                "gasUsed": int(block["gasUsed"], 16),
                "txCount": len(block["transactions"])
            })
            print(f"🔄 Block {block_num} mirrored")

        time.sleep(0.3)

    with open("block_log.json", "w") as f:
        json.dump(mirrored, f, indent=2)
    print(f"\n✅ Saved {len(mirrored)} blocks to block_log.json")

if __name__ == "__main__":
    mirror_blocks(10)
