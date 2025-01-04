# Cellular Automata
<p align="center">
  <img src="./Examples/Data/life/seeds/seeds-7fps.gif" width = "50%">
</p>

A cell can be either alive or dead, and its next state depend on a set of rules applied on its neighbor cells. The number of possible sets are determined by the *recognized* neighbors of the cell. In this repository we present two modules for the elementary and life-like cases. The first is in $1\rm D$ and takes $2$ neighbors (left and right) into account, while the second is in $2\rm D$ and uses the Moore neighbourhood ($8$ individuals). **The methods developed make it possible for all possible sets of rules to be implemented because of binary encoding.**

## Elementary case

This is the $1\rm D$ case, the simplest. The image below shows the evolution of one of the possible $256$ sets of rules with different binary input arrays. The module `elementary.py` contains the class `ElementaryCA` from which any of the $256$ sets can be easily implemented. Examples can be found in `Examples/01-Elementary-CA.ipynb`.

<p align="center">
  <img src="./Data/output-75/evolution-rule-75.gif" width = "60%">
</p>

## Life-like case
