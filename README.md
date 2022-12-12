# emoji-chem  [![build](https://github.com/whitead/emoji-chem/actions/workflows/tests.yml/badge.svg)](https://whitead.github.io/emoji-chem/)[![PyPI version](https://badge.fury.io/py/emoji-chem.svg)](https://badge.fury.io/py/emoji-chem)


[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/whitead/emoji-chem/blob/main/colab/EmojiChem.ipynb)

## Install

```sh
pip install emojichem
```

## Quickstart

*Note: this is currently broken -- it mixes up order of hydrogens and heteroatoms on side groups (e.g., NH2 or OH). Not sure how to fix this because rdkit doesn't output enough information for me rewrite the SVG.*

```py
import emojichem
emojichem.emoji_draw('CCN(CC)C(=O)[C@H]1CN([C@@H]2Cc3c[nH]c4c3c(ccc4)C2=C1)C')
```

## Example
This is how it should look

![image](https://user-images.githubusercontent.com/908389/206943965-f57686f9-554b-476d-9f8a-24121206fce4.png)


## Credit
Emoji list was taken (with minor modifications) from Nicola Ga-stan (@nicgaston) in [this tweet](https://twitter.com/nicgaston/status/914311195305193472)
