from .data import elem_dict, emoji_dict
from rdkit import Chem
from rdkit.Chem import Draw
import xml.etree.ElementTree as ET
from .version import __version__


def emoji_draw(mol, filename=None, width=300, height=200):
    if type(mol) is str:
        mol = Chem.MolFromSmiles(mol)
    drawer = Chem.Draw.rdMolDraw2D.MolDraw2DSVG(width, height)
    drawer.drawOptions().bgColor = None
    drawer.drawOptions().baseFontSize = 1.0
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    sp = {}

    for a in Chem.AddHs(mol).GetAtoms():
        sp[f"atom-{a.GetIdx()}"] = emoji_dict[elem_dict[a.GetSymbol()]]
    svg_data = rewrite_svg(drawer.GetDrawingText(), sp)
    if filename is not None:
        with open(filename, "w") as f:
            f.write(svg_data)
    # try to display with ipython
    try:
        from IPython.display import SVG

        return SVG(svg_data)
    except ImportError:
        return svg_data


def extract_size(path):
    spath = path.split()
    x, y = [], []
    for i in range(0, len(spath), 3):
        if spath[i] == "M" or spath[i] == "L":
            x.append(float(spath[i + 1]))
            y.append(float(spath[i + 2]))
        elif spath[i] == "Q":
            x.append(float(spath[i + 3]))
            y.append(float(spath[i + 4]))
    dx = max(x) - min(x)
    dy = max(y) - min(y)
    return str(min(x) + dx / 2), str(min(y)), str(dx), str(dy)


def rewrite_svg(svg, sp):
    root = ET.fromstring(svg)
    SVGNS = "http://www.w3.org/2000/svg"
    marked = {}
    undo = dict()
    update = []
    for p in root.findall(".//{http://www.w3.org/2000/svg}path"):
        try:
            name = p.attrib["class"]
        except KeyError:
            continue
        if name in sp:
            if name in marked:
                # check if we need to go back because previous was integer
                if marked[name][0] == 1:
                    # reset fill
                    del undo[name][0].attrib["fill"]
                    ET.SubElement(root, undo[name][0].tag, undo[name][0].attrib)
                    root.remove(undo[name][1])
                    update.remove(undo[name][1])

                x, y, dx, dy = extract_size(p.attrib["d"])
                t = ET.SubElement(
                    root,
                    "{http://www.w3.org/2000/svg}text",
                    {
                        "x": x,
                        "y": y,
                        "font-size": marked[name][1],
                        "text-anchor": "middle",
                        "dominant-baseline": "hanging",
                        "textLength": dx,
                    },
                )
                t.text = emoji_dict["hydrogen"]
                marked[name][0] += 1
                update.append(t)
                # could be digit
                undo = {name: (p, t)}
            else:
                x, y, dx, dy = extract_size(p.attrib["d"])
                t = ET.SubElement(
                    root,
                    "{http://www.w3.org/2000/svg}text",
                    {
                        "x": x,
                        "y": y,
                        "font-size": dy,
                        "text-anchor": "middle",
                        "dominant-baseline": "hanging",
                        "textLength": dx,
                    },
                )
                t.text = sp[name]
                marked[name] = [0, dy]
                update.append(t)
            root.remove(p)
    # go through and get max font size
    max_font = 1
    for t in update:
        max_font = max(max_font, float(t.attrib["font-size"]))
    for t in update:
        t.attrib["font-size"] = str(max_font)
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    return ET.tostring(root, encoding="unicode", method="xml")
