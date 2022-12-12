from rdkit import Chem
import emojichem


def test_emojichem():
    mol = Chem.MolFromSmiles("O=C(NCC1CCCCC1N)C2=CC=CC=C2C3=CC=C(F)C=C3C(=O)NC4CCCCC4")
    emojichem.emoji_draw(mol, "wow.svg")


def test_emojichem_str():
    emojichem.emoji_draw("O=C(NCC1CCCCC1N)C2=CC=CC=C2C3=CC=C(F)C=C3C(=O)NC4CCCCC4")


def test_emojichem_grid():
    smiles = """Oc1ccc(N2CCNCC2)cc1
    Cc1n[nH]c(C)c1CCN
    C[C@H](C(=O)O)[C@H](C)C(=O)O
    CSCCCN
    COC(=O)c1cc(C=O)ccc1O
    CC(C)(N)C(=O)N1CCCCC1
    N[C@H]1CCCC(=O)C1
    NC(=O)CCOc1ccccc1N
    Cc1ncc(CO)s1
    CC(C)n1cncn1
    COC(=O)c1cc(N)cc2cn[nH]c12
    C[C@H](c1cnn(C)c1)n1nccc1N
    C[C@@H]1CCS1(=O)=O
    COCCOc1cnc(N)cn1
    CNc1cnc(C)cn1
    N=C(N)c1scc2c1OCCO2
    C[C@@H]1COC[C@@H](C)N1CCCN
    COC[C@H](N)[C@]1(O)CCS[C@H]1C
    CCN(CC)C(N)=O
    CCc1nsc(N)n1
    NC(=S)Nc1cnccn1
    Cc1nn(C)cc1/C=C/C(=O)O""".split(
        "\n"
    )

    emojichem.emoji_grid(smiles)
