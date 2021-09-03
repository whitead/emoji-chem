from rdkit import Chem
import emojichem


def test_emojichem():
    mol = Chem.MolFromSmiles(
        'O=C(NCC1CCCCC1N)C2=CC=CC=C2C3=CC=C(F)C=C3C(=O)NC4CCCCC4')
    emojichem.emoji_draw(mol, 'wow.svg')
