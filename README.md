# emoji-chem
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/whitead/emoji-chem/blob/main/colab/EmojiChem.ipynb)

```py
from rdkit import Chem
import emojichem
mol = Chem.MolFromSmiles('O=C(NCC1CCCCC1N)C2=CC=CC=C2C3=CC=C(F)C=C3C(=O)NC4CCCCC4')
emojichem.emoji_draw(mol, 'wow.svg')

# in jupyter notebook
from IPython.display import SVG, display

svg = emojichem.emoji_draw(mol)
display(SVG(svg))
```

## Example
This is how it should look

![image](https://user-images.githubusercontent.com/908389/131951211-ef0047c9-3ced-4967-ae84-0f76c9ff16ea.png?width=40px)


## Credit
Emoji list was taken (with minor modifications) from Nicola Ga-stan (@nicgaston) in [this tweet](https://twitter.com/nicgaston/status/914311195305193472)