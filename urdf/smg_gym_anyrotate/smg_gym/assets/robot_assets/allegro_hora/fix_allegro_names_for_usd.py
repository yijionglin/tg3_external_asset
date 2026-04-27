from xml.etree import ElementTree as ET

INPUT = "/home/bourne/smg_gym_anyrotate/smg_gym/assets/robot_assets/allegro_hora/allegro_isaacsim_fixed.urdf"
OUTPUT = "/home/bourne/smg_gym_anyrotate/smg_gym/assets/robot_assets/allegro_hora/allegro_isaacsim_usd_safe.urdf"

tree = ET.parse(INPUT)
root = tree.getroot()

def sanitize(name: str) -> str:
    return name.replace(".", "_")

# 1. Rename links
link_name_map = {}
for link in root.findall("link"):
    old = link.attrib["name"]
    new = sanitize(old)
    link_name_map[old] = new
    link.attrib["name"] = new

# 2. Rename joints and update parent/child refs
for joint in root.findall("joint"):
    joint.attrib["name"] = sanitize(joint.attrib["name"])

    parent = joint.find("parent")
    child = joint.find("child")

    if parent is not None:
        parent.attrib["link"] = sanitize(parent.attrib["link"])
    if child is not None:
        child.attrib["link"] = sanitize(child.attrib["link"])

# 3. Fix visual & collision names (optional but safe)
for tag in ["visual", "collision"]:
    for elem in root.findall(f".//{tag}"):
        if "name" in elem.attrib:
            elem.attrib["name"] = sanitize(elem.attrib["name"])

tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
print(f"Wrote {OUTPUT}")