Python program that makes a decision tree using the Training Set, has the option to prune the tree using the Validation Set, and tests the tree with the Test Set.  It tests the data using the information gain heuristic, and the variance impurity heuristic.  It also includes the option to print the decision tree.

To run:
python decisionTree.py <Training_Set> <Validation_Set> <Test_Set> <to_print = {yes, no}> <prune = {yes, no}>

Results:
D1:
H1 NP Training 1.0
H1 NP Validation 0.953333333333
H1 NP Testing 0.94
H1 P Training 0.951666666667
H1 P Validation 0.963333333333
H1 P Testing 0.926666666667
H2 NP Training 1.0
H2 NP Validation 0.965
H2 NP Testing 0.95
H2 P Training 0.996666666667
H2 P Validation 0.965
H2 P Testing 0.948333333333
D2:
H1 NP Training 0.998333333333
H1 NP Validation 0.75
H1 NP Testing 0.758333333333
H1 P Training 0.866666666667
H1 P Validation 0.815
H1 P Testing 0.776666666667
H2 NP Training 0.998333333333
H2 NP Validation 0.705
H2 NP Testing 0.698333333333
H2 P Training 0.858333333333
H2 P Validation 0.786666666667
H2 P Testing 0.72