from xml.etree import ElementTree as ET
from pathlib import Path

INPUT = "/home/bourne/smg_gym_anyrotate/smg_gym/assets/robot_assets/allegro_hora/allegro_isaacsim_usd_safe.urdf"
OUTPUT = "/home/bourne/smg_gym_anyrotate/smg_gym/assets/robot_assets/allegro_hora/allegro_isaacsim_usd_final.urdf"

def sanitize(name: str) -> str:
    return name.replace(".", "_")

tree = ET.parse(INPUT)
root = tree.getroot()

for link in root.findall("link"):
    link_name = link.attrib["name"]

    for tag in ["visual", "collision"]:
        for i, elem in enumerate(link.findall(tag)):
            # Force a USD-safe name
            elem.attrib["name"] = f"{link_name}_{tag}_{i}"

            geom = elem.find("geometry")
            if geom is not None:
                mesh = geom.find("mesh")
                if mesh is not None and "filename" in mesh.attrib:
                    # Optional but recommended: sanitize mesh basename
                    p = Path(mesh.attrib["filename"])
                    safe_name = sanitize(p.stem) + p.suffix
                    mesh.attrib["filename"] = str(p.parent / safe_name)

tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
print(f" Wrote {OUTPUT}")
