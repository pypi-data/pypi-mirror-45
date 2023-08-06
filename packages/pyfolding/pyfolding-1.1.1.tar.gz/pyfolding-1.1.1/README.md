# python3-libfolding/pyfolding

Ths repository gathers python3 bindings to `libfolding`, a library performing the Folding Test of Unimodality (FTU) on both batch and streaming data.

For more details about `libfolding` and the FTU, visit https://asiffer.github.io/libfolding

## Installation

You can download it through `apt` (it will automatically download `libfolding`)
```shell
$ sudo add-apt-repository ppa:asiffer/libfolding
$ sudo apt-get update
$ sudo apt-get install python3-libfolding
```

Otherwise, it is also available on PyPI (but you must install `libfolding` independently)
```shell
$ pip3 install pyfolding
```

## Usage

### Batch

The first thing you probably want to do is to check is a dataset is unimodal. `pyfolding` embeds the `FTU` function which does the job. You can either choose 
the pure python implementation (`routine="python"`) or the wrapper around the `C++` native implementation (`routine="c++"`).

WARNING: The results of the two routines may be slightly different.

```python
import pyfolding as pf
import numpy as np

# 1D example
X = np.random.normal(0, 1, 2000)
results = pf.FTU(X, routine="python")
print(results)
```

The output may look like the following:
```shell
           #observations: 2000
                     dim: 1
                    Φ(X): 1.436777489
                    φ(X): 0.359194372
         folded variance: 0.343085433
           folding pivot: [-0.02638367]
                 p-value: 0.000065827
                    time: 0.000453949
                 message: 
```

The results gather quite everything about the test. The most important field is the folding statistics Φ(X). If it is greater than 1, the dataset is then unimodal, otherwise it is multimodal. We can tackle more complex datasets:

```python
import pyfolding as pf
from sklearn.datasets import make_blobs
import numpy as np

# 2D example (3000 points, dimension 3, 2 clusters)
X,_ = make_blobs(n_samples=3000, n_features=3, centers=2, random_state=42)
results = pf.FTU(X, routine="cpp")
print(results)
```

The output may look like as below. We can check that the folding statistic Φ(X) is lower than 1, so the distribution is multimodal.
```shell
           #observations: 3000
                     dim: 3
                    Φ(X): 0.157387899
                    φ(X): 0.009836744
         folded variance: 1.027833560
           folding pivot: [-0.31059918  1.08473035 -1.16174564]
                 p-value: 0.000000000
                    time: 0.000575000
                 message: 
```

### Streaming

One of the main feature of the FTU is the ability to be computed/updated over streaming data.

```python
import pyfolding as pf
import numpy as np
import matplotlib.pyplot as plt

def data_generator(n: int, speed: int=1e-3, std: float=1.0):
    mu0 = np.array([-5,5])
    v0 = np.array([1,-1])/np.sqrt(2)
    mu1 = np.array([5,5])
    v1 = np.array([-1,-1])/np.sqrt(2)
    X = np.random.multivariate_normal([0, 0], std * np.eye(2), n)
    e = np.random.uniform(-1, 1, n)
    for i in range(n):
        if e[i]>0:
            yield X[i] + (mu0 + v0 * speed * i)
        else:
            yield X[i] + (mu1 + v1 * speed * i)

depth = 500
sf = pf.StreamFolding(depth) 
phi = []
for i,x in enumerate(data_generator(20000, speed=0.001)):
    sf.update(x)
    if i>depth and i % 50 == 0:
        r = sf.folding_test()
        phi.append(r.folding_statistics)

plt.plot(phi)
```