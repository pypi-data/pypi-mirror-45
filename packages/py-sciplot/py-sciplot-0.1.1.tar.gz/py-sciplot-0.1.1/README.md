=======
sciplot
=======


Style and plotting tools for matplotlib.



Installation
============

```bash

python3 ./setup.py develop --user

```

The matolotlib style can be installed in the sytlelib folder:

```bash

./install_mlp_style.sh

```

Usage
=====

After installation you can use the style with matplotlib:

```python

import matplotlib.pyplot as plt

plt.style.use('sciplot')

```


To use the library you can do

```python

import sciplot

sciplot.hist([1,2])

```

![Example](examples/stacked_plot.png?raw=true "Title")
