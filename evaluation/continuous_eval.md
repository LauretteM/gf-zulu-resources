# Continuous evaluation protocol

Continuous evaluation consists of two steps:
1. Regression testing
2. gftest

Regression testing ensures that the latest RG performs as expected on a specific set of trees. gftest generates new trees with their linearisations, which are manually evaluated.

## 1. Regression test

Regression testing is done on regression.treebank. In the event that certain tree-linearisation pairs fail, there are two possible causes:
1. If caused by an error in the grammar, the grammar must be fixed.
2. If caused by a deprecation of the tree, the tree-linearisation pair must be removed.

Once the regression test succeeds on all pairs in regression.treebank, step 2 can be performed.

## 2. gftest

gftest is relied on to generate a minimal and representative set of tree-linearisation pairs for the grammar. These are manually evaluated.
1. In cases where tree-linearisation pairs are evaluated as correct, these pairs are added to regression.treebank.
2. In cases where tree-linearisation pairs are evaluated as incorrect
    - a hand-crafted tree-linearisation pair can be added to regression.treebank
    - notes on ways the grammar must be fixed/improved form the basis of the next iteration
