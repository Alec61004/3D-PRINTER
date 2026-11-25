import struct
import json
from pathlib import Path

def inspect_glb(glb_path):
    with open(glb_path, "rb") as f:
        data = f.read()

    magic, version, length = struct.unpack_from("<4sII", data, 0)
    print(f"File: {glb_path}")
    print(f"Magic: {magic.decode('ascii')}, Version: {version}, Length: {length} (File size: {len(data)})")
    
    offset = 12
    json_chunk = None
    while offset < len(data):
        chunk_len, chunk_type = struct.unpack_from("<I4s", data, offset)
        type_str = chunk_type.decode("ascii")
        if type_str == "JSON":
            json_bytes = data[offset+8 : offset+8+chunk_len]
            json_chunk = json.loads(json_bytes.decode("utf-8"))
        offset += 8 + chunk_len

    if json_chunk:
        node_names = [n.get("name", "") for n in json_chunk.get("nodes", [])]
        print(f"Total nodes ({len(node_names)}): {node_names}")
        required = ['enclosure', 'door', 'printHead', 'printBed', 'front_glass_door']
        missing = [r for r in required if r not in node_names]
        print(f"Missing required nodes: {missing}")
        if missing:
            raise ValueError(f"Missing nodes: {missing}")
        print("ALL REQUIRED NODES PRESENT AND VALID!")
    else:
        print("No JSON chunk found!")

if __name__ == "__main__":
    inspect_glb("assets/models/raw/deltrol_p2s_unibody_pivoted.glb")
