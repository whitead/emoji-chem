from .data import elem_dict, emoji_dict
from rdkit import Chem
from rdkit.Chem import Draw
import xml.etree.ElementTree as ET


def emoji_draw(mol, filename, width=300, height=200):
    drawer = Chem.Draw.rdMolDraw2D.MolDraw2DSVG(width, height)
    drawer.drawOptions().bgColor = None
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    sp = {}
    for a in mol.GetAtoms():
        if a.GetSymbol() != 'C':
            sp[f'atom-{a.GetIdx()}'] = emoji_dict[elem_dict[a.GetSymbol()]]
    svg = rewrite_svg(drawer.GetDrawingText(), sp)
    with open(filename, 'w') as f:
        f.write(svg)


def extract_mins(path):
    spath = path.split()
    x, y = [], []
    for i in range(0, len(spath), 3):
        if spath[i] == 'M' or spath[i] == 'L':
            x.append(float(spath[i + 1]))
            y.append(float(spath[i + 2]))
    dx = max(x) - min(x)
    return str(min(x) + dx), str(min(y)), str(dx)


def rewrite_svg(svg, sp):
    root = ET.fromstring(svg)
    SVGNS = u"http://www.w3.org/2000/svg"
    marked = {}
    for p in root.findall('.//{http://www.w3.org/2000/svg}path'):
        name = p.attrib['class']
        if name in sp:
            if name in marked:
                x, y, dx = extract_mins(p.attrib['d'])
                marked[name].text = emoji_dict['hydrogen'] + marked[name].text
                marked[name].attrib['textLength'] = str(
                    float(marked[name].attrib['textLength']) + float(dx))
            else:
                x, y, dx = extract_mins(p.attrib['d'])
                t = ET.SubElement(
                    root,
                    '{http://www.w3.org/2000/svg}text',
                    {
                        'x': x,
                        'y': y,
                        'font-size': '0.8rem',
                        'dominant-baseline': 'middle',
                        'text-anchor': 'middle', 'textLength': dx
                    })
                t.text = sp[name]
                marked[name] = t
            root.remove(p)
    return ET.tostring(root, encoding="unicode", method='xml')
