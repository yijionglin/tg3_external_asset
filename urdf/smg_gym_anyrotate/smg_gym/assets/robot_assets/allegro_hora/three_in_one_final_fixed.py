from xml.etree import ElementTree as ET
from pathlib import Path

INPUT_URDF = "/home/bourne/smg_gym_anyrotate/smg_gym/assets/robot_assets/allegro_hora/allegro_digitac_v2_inw_90_45_90.urdf"
OUTPUT_URDF = "/home/bourne/smg_gym_anyrotate/smg_gym/assets/robot_assets/allegro_hora/allegro_digitac_v2_inw_90_45_90_isaacsim_ready.urdf"

def sanitize(name: str) -> str:
    return name.replace(".", "_")

tree = ET.parse(INPUT_URDF)
root = tree.getroot()

# 1. Fix link names
for link in root.findall("link"):
    link.attrib["name"] = sanitize(link.attrib["name"])

# 2. Fix joint names + parent/child refs
for joint in root.findall("joint"):
    joint.attrib["name"] = sanitize(joint.attrib["name"])

    parent = joint.find("parent")
    child = joint.find("child")

    if parent is not None:
        parent.attrib["link"] = sanitize(parent.attrib["link"])
    if child is not None:
        child.attrib["link"] = sanitize(child.attrib["link"])

# 3. Force USD-safe visual & collision names
for link in root.findall("link"):
    lname = link.attrib["name"]

    for tag in ["visual", "collision"]:
        for i, elem in enumerate(link.findall(tag)):
            elem.attrib["name"] = f"{lname}_{tag}_{i}"

            geom = elem.find("geometry")
            if geom is not None:
                mesh = geom.find("mesh")
                if mesh is not None and "filename" in mesh.attrib:
                    p = Path(mesh.attrib["filename"])
                    mesh.attrib["filename"] = str(p.parent / (sanitize(p.stem) + p.suffix))

tree.write(OUTPUT_URDF, encoding="utf-8", xml_declaration=True)
print(f"✅ Wrote {OUTPUT_URDF}")
