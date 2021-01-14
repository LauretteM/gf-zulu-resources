# Continuous evaluation

## Protocol outline

Continuous evaluation consists of two steps:
1. Regression testing
2. gftest

Regression testing ensures that the latest RG performs as expected on a specific set of trees. gftest generates new trees with their linearisations, which are manually evaluated.

### 1. Regression test

Regression testing is done on `gf-zulu-resources/treebanks/regression.treebank` using `gf-zulu-resources/lexica/test/Test.pgf`. In the event that certain tree-linearisation pairs fail, there are two possible causes:
1. If caused by an error in the grammar, the grammar must be fixed.
2. If caused by a deprecation of the tree, the tree-linearisation pair must be removed.

Once the regression test succeeds on all pairs in `regression.treebank`, step 2 can be performed.

### 2. gftest

gftest is relied on to generate a minimal and representative set of tree-linearisation pairs for the grammar. These are manually evaluated.
1. In cases where tree-linearisation pairs are evaluated as correct, these pairs are added to `regression.treebank`.
2. In cases where tree-linearisation pairs are evaluated as incorrect,
    - a correct, hand-crafted tree-linearisation pair can be added to `regression.treebank`
    - notes on ways the grammar must be fixed/improved form the basis of the next iteration

## Detailed workflow

All the commands in this section use paths relative to the evaluation folder. It also assumes that the `gf-rgl-zul` folder is in the same location as `gf-zulu-resources`.
```Shell
$ cd $WORKDIR/gf-zulu-resources/evaluation
```

### PGF prep

Compile the grammar with the test lexicon.
```Shell
$ gf --make --optimize-pgf --path=$WORKDIR/gf-rgl-zul/src/* --output-dir=../lexica/test ../lexica/test/TestZul.gf
```

### 1. Regression test

Perform the regression test.
```Shell
$ python3 evaltools.py regression ../lexica/test/Test.pgf ../treebanks/regression.treebank
```

### 2. gftest

Run gftest with a chosen function (or list of functions) and label the output.
```Shell
$ FUNCTIONS="UseV UseN"
$ LABEL=UseV_UseN.2021-01-01

$ gftest -g ../lexica/test/Test.pgf -l Zul -f $FUNCTIONS > tests/TestZul_$LABEL.txt
```

### Document prep

Prepare the output of gftest for the reviewer.

```Shell
$ python3 evaltools.py viz_gftest tests/TestZul_$LABEL.txt ../lexica/test/Test.pgf -d tests/
$ wkhtmltopdf tests/TestZul_$LABEL.html tests/TestZul_$LABEL.pdf
```
