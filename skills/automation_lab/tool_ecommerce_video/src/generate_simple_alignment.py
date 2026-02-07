import json
import os
import sys

def generate_alignment(text_file, duration, output_file):
    with open(text_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    num_lines = len(lines)
    duration_per_line = duration / num_lines
    
    fragments = []
    current_time = 0.0
    
    for i, line in enumerate(lines):
        start = current_time
        end = current_time + duration_per_line
        fragments.append({
            "begin": f"{start:.3f}",
            "end": f"{end:.3f}",
            "id": f"f{i:06d}",
            "language": "pt",
            "lines": [line]
        })
        current_time = end

    data = {"fragments": fragments}
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Generated alignment for {num_lines} lines over {duration} seconds.")

if __name__ == "__main__":
    if len(sys.argv) > 3:
        text_file = sys.argv[1]
        duration = float(sys.argv[2])
        output_file = sys.argv[3]
    else:
        text_file = "skills/automation_lab/tool_ecommerce_video/disk_uniformes/spoken_script/spoken_script.txt"
        output_file = "skills/automation_lab/tool_ecommerce_video/disk_uniformes/aligned_script_with_timestamps/aligned_output.json"
        duration = 18.102177
    
    generate_alignment(text_file, duration, output_file)
