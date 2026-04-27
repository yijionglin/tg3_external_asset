from xml.etree import ElementTree as ET

tree = ET.parse("/home/bourne/smg_gym_anyrotate/smg_gym/assets/robot_assets/allegro_hora/allegro_digitac_v2_inw_90_45_90.urdf")
root = tree.getroot()

def make_default_inertial():
    inertial = ET.Element("inertial")
    ET.SubElement(inertial, "origin", xyz="0 0 0", rpy="0 0 0")
    ET.SubElement(inertial, "mass", value="0.01")
    ET.SubElement(
        inertial,
        "inertia",
        ixx="1e-5", ixy="0", ixz="0",
        iyy="1e-5", iyz="0", izz="1e-5",
    )
    return inertial

for link in root.findall("link"):
    inertial = link.find("inertial")
    if inertial is None:
        link.append(make_default_inertial())
    else:
        mass = inertial.find("mass")
        if mass is None or float(mass.attrib.get("value", "0")) <= 0:
            if mass is None:
                mass = ET.SubElement(inertial, "mass")
            mass.attrib["value"] = "0.01"

tree.write("allegro_isaacsim_fixed.urdf",
           encoding="utf-8",
           xml_declaration=True)

print("Wrote allegro_isaacsim_fixed.urdf")