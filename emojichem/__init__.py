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


def extract_atom_size(path):
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
    return min(x), min(y), dx, dy


def extract_bond_size(path):
    spath = path.replace(",", " ").split()
    # just iterate through assuming M, x, y, L, x, y
    x0 = float(spath[1])
    y0 = float(spath[2])
    x1 = float(spath[4])
    y1 = float(spath[5])
    dx = x1 - x0
    dy = y1 - y0
    return x0, y0, dx, dy


def rewrite_svg(svg, sp):
    root = ET.fromstring(svg)
    SVGNS = "http://www.w3.org/2000/svg"
    marked = {}
    update = []
    bonds = {}

    # this code is to find bond positions related to an atom
    for p in root.findall(".//{http://www.w3.org/2000/svg}path"):
        try:
            name = p.attrib["class"]
        except KeyError:
            continue
        # check if it's a bond that matches our atoms
        if "bond" not in name:
            continue
        atoms = []
        for s in sp:
            if s in name:
                atoms.append(s)
        if len(atoms) > 0:
            x, y, dx, dy = extract_bond_size(p.attrib["d"])
            for a in atoms:
                if a in bonds:
                    bonds[a].append((x, y, dx, dy))
                else:
                    bonds[a] = [(x, y, dx, dy)]
    # now find which atom element is closest to a bond (and mark it)
    scores = {n: [] for n in sp}
    for p in root.findall(".//{http://www.w3.org/2000/svg}path"):
        try:
            name = p.attrib["class"]
        except KeyError:
            continue
        if name in sp and name in bonds:
            # get min distance to bond
            x, y, _, _ = extract_atom_size(p.attrib["d"])
            mind = 1000000
            for b in bonds[name]:
                bx, by, _, _ = b
                mind = min(mind, (bx - x) ** 2 + (by - y) ** 2)
            scores[name].append((mind, p))
    # now mark the closest element
    for n in scores:
        if len(scores[n]) < 2:
            continue
        scores[n].sort(key=lambda x: x[0])
        marked[n] = scores[n][0][1]
    for p in root.findall(".//{http://www.w3.org/2000/svg}path"):
        try:
            name = p.attrib["class"]
        except KeyError:
            continue
        if name in sp:
            if name in marked and p != marked[name]:
                # not closest heavy
                x, y, dx, dy = extract_atom_size(p.attrib["d"])
                # estimate if it's an integer by looking for subscript
                x0, y0, dx0, dy0 = extract_atom_size(marked[name].attrib["d"])
                # some heuristic for subscript
                if 1 < y - y0 and (y - y0 - dy0) ** 2 / dy0**2 < 0.1:
                    # just adjust font size
                    p.attrib["font-size"] = str(dy0 / 2)
                    continue
                t = ET.SubElement(
                    root,
                    "{http://www.w3.org/2000/svg}text",
                    {
                        "x": str(x + dx / 2),
                        "y": str(y),
                        "font-size": str(dy),
                        "text-anchor": "middle",
                        "dominant-baseline": "hanging",
                        "textLength": str(dx),
                    },
                )
                t.text = emoji_dict["hydrogen"]
                update.append(t)
            else:
                x, y, dx, dy = extract_atom_size(p.attrib["d"])
                t = ET.SubElement(
                    root,
                    "{http://www.w3.org/2000/svg}text",
                    {
                        "x": str(x + dx / 2),
                        "y": str(y),
                        "font-size": str(dy),
                        "text-anchor": "middle",
                        "dominant-baseline": "hanging",
                        "textLength": str(dx),
                    },
                )
                t.text = sp[name]
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
