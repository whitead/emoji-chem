from .data import elem_dict, emoji_dict
from rdkit import Chem
from rdkit.Chem import Draw
import xml.etree.ElementTree as ET
from .version import __version__
import skunk


def emoji_grid(mols, labels=None, filename=None):
    svgs = []
    for m in mols:
        if type(m) is str:
            m = Chem.MolFromSmiles(m)
        svgs.append(
            emoji_draw(m, filename=None, width=200, height=200, return_svg=True)
        )
    svg_data = skunk.layout_svgs(svgs, labels=labels)
    if filename is not None:
        with open(filename, "w") as f:
            f.write(svg_data)
    # try to display with ipython
    try:
        from IPython.display import SVG

        return SVG(svg_data)
    except ImportError:
        return svg_data


def emoji_draw(mol, filename=None, width=300, height=200, return_svg=False):
    if type(mol) is str:
        mol = Chem.MolFromSmiles(mol)
    drawer = Chem.Draw.rdMolDraw2D.MolDraw2DSVG(width, height)
    drawer.drawOptions().bgColor = None
    drawer.drawOptions().baseFontSize = 1.0
    drawer.drawOptions().drawMolsSameScale = False
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
    if not return_svg:
        try:
            from IPython.display import SVG

            return SVG(svg_data)
        except ImportError:
            pass
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
    update = []
    for p in root.findall(".//{http://www.w3.org/2000/svg}path"):
        try:
            name = p.attrib["class"]
        except KeyError:
            continue
        if name in sp:
            if name in marked:
                x, y, dx, dy = extract_size(p.attrib["d"])
                # estimate if it's an integer by looking for subscript
                yf = float(y)
                y0f = float(marked[name].attrib["y"])
                dy0f = float(marked[name].attrib["font-size"])
                if 1 < yf - y0f < dy0f:
                    # just adjust font size
                    marked[name].attrib["font-size"] = str(
                        float(marked[name].attrib["font-size"]) * 0.5
                    )
                    continue
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
                t.text = emoji_dict["hydrogen"]
                update.append(t)
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
                marked[name] = t
                update.append(t)
            root.remove(p)
    # go through and get avg font size
    font_size = 0
    for t in update:
        font_size += float(t.attrib["font-size"])
    for t in update:
        t.attrib["font-size"] = str(font_size / len(update))
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    return ET.tostring(root, encoding="unicode", method="xml")
