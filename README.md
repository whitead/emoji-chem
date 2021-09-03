# emoji-chem
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/whitead/emoji-chem/blob/main/colab/EmojiChem.ipynb)

```py
from rdkit import Chem
import emojichem
mol = Chem.MolFromSmiles('O=C(NCC1CCCCC1N)C2=CC=CC=C2C3=CC=C(F)C=C3C(=O)NC4CCCCC4')
emojichem.emoji_draw(mol, 'wow.svg')
```
