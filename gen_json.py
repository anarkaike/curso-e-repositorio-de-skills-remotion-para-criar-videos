import json
import os

duration = 18.10
lines = [
    "Procurando uniformes de qualidade para sua empresa?",
    "Na Disk Uniformes você encontra a solução completa.",
    "Temos linha médica, gastronômica e corporativa.",
    "Personalize com sua marca e vista sua equipe com estilo.",
    "Entre em contato e faça seu orçamento agora!"
]

fragment_duration = duration / len(lines)
fragments = []

for i, line in enumerate(lines):
    start = i * fragment_duration
    end = (i + 1) * fragment_duration
    fragments.append({
        "begin": f"{start:.3f}",
        "end": f"{end:.3f}",
        "id": f"f{i:06d}",
        "language": "pt",
        "lines": [line]
    })

data = {"fragments": fragments}

output_dir = "skills/automation_lab/tool_ecommerce_video/disk_uniformes/aligned_script_with_timestamps"
os.makedirs(output_dir, exist_ok=True)
with open(os.path.join(output_dir, "aligned_output.json"), "w") as f:
    json.dump(data, f, indent=4)
print("JSON generated")
