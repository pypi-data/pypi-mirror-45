# wittgenstein

_And is there not also the case where we play and--make up the rules as we go along?
  -Ludwig Wittgenstein_

![the duck-rabbit](https://github.com/imoscovitz/wittgenstein/blob/master/duck-rabbit.jpg)

## Summary

This package implements two iterative coverage-based ruleset algorithms: IREP and RIPPERk.

Performance is similar to sklearn's DecisionTree CART implementation (see [Performance Tests](https://github.com/imoscovitz/ruleset/blob/master/Performance%20Tests.ipynb)).

For explanation of the algorithms, see my article in _Towards Data Science_, or the papers below, under [Useful References](https://github.com/imoscovitz/wittgenstein#useful-references).

## Installation

To install, use
```bash
$ pip install wittgenstein
```

To uninstall, use
```bash
$ pip uninstall wittgenstein
```

## Usage

Usage syntax is similar to sklearn's. The current version, however, does require that data be passed in as a Pandas DataFrame.

Once you have loaded and split your data...
```python
>>> import pandas as pd
>>> df = pd.read_csv(dataset_filename)
>>> from sklearn.model_selection import train_test_split # Or any other mechanism you want to use for data partitioning
>>> train, test = train_test_split(df, test_size=.33)
```
We can fit a ruleset classifier using RIPPER or IREP.
```python
>>> import wittgenstein as lw
>>> ripper_clf = lw.RIPPER() # Or irep_clf = lw.IREP() to build a model using IREP
>>> ripper_clf.fit(train, class_feat='Party') # Or call .fit with params train_X, train_y
>>> ripper_clf
<RIPPER object with fit ruleset (k=2, prune_size=0.33, dl_allowance=64)> # Hyperparameter details available in the docstrings and TDS article below
```

Access the underlying trained model with the ruleset_ attribute. A ruleset is a disjunction of conjunctions -- 'V' represents 'or'; '^' represents 'and'.

In other words, the model predicts positive class if any of the inner-nested condition-combinations are all true:
```python
>>> ripper_clf.ruleset_
<Ruleset object: [physician-fee-freeze=n] V [synfuels-corporation-cutback=y^adoption-of-the-budget-resolution=y^anti-satellite-test-ban=n]>
```
To score our fit model:
```python
>>> test_X = test.drop(class_feat, axis=1)
>>> test_y = test[class_feat]
>>> ripper_clf.score(test_X, test_y)
0.9985686906328078
```
Default scoring metric is accuracy. You can pass in alternate scoring functions, including those available through sklearn:
```python
from sklearn.metrics import precision_score, recall_score
>>> precision = clf.score(X_test, y_test, precision_score)
>>> recall = clf.score(X_test, y_test, recall_score)
>>> print(f'precision: {precision} recall: {recall})
precision: 0.9914..., recall: 0.9953...
```
To perform predictions:
```python
>>> ripper_clf.predict(new_data)[:5]
[True, True, False, True, False]
```
We can also ask our model to tell us why it made each positive prediction that it did:
```python
>>> ripper_clf.predict(new_data)[:5]
([True, True, False, True, True]
[<Rule object: [physician-fee-freeze=n]>],
[<Rule object: [physician-fee-freeze=n]>,
  <Rule object: [synfuels-corporation-cutback=y^adoption-of-the-budget-resolution=y^anti-satellite-test-ban=n]>], # This example met multiple sufficient conditions for a positive prediction
[],
[<Rule object: [physician-fee-freeze=n]>],
[])
```

## Issues
If you encounter any issues, or if you have feedback or improvement requests for how wittgenstein could be made more helpful for you, please post them to [issues](https://github.com/imoscovitz/wittgenstein/issues), and I'll respond.

## Contributing
Contributions are welcome! If you are interested in contributing, let me know at ilan.moscovitz@gmail.com or on [linkedin](https://www.linkedin.com/in/ilan-moscovitz/).

## Useful references
- [My article in _Towards Data Science_ explaining IREP, RIPPER, and wittgenstein](https://towardsdatascience.com/how-to-perform-explainable-machine-learning-classification-without-any-trees-873db4192c68)
- [Furnkrantz-Widmer IREP paper](https://pdfs.semanticscholar.org/f67e/bb7b392f51076899f58c53bf57d5e71e36e9.pdf)
- [Cohen's RIPPER paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.107.2612&rep=rep1&type=pdf)
- [Partial decision trees](https://researchcommons.waikato.ac.nz/bitstream/handle/10289/1047/uow-cs-wp-1998-02.pdf?sequence=1&isAllowed=y)
- [Bayesian Rulesets](https://pdfs.semanticscholar.org/bb51/b3046f6ff607deb218792347cb0e9b0b621a.pdf)
- [C4.5 paper including all the gory details on MDL](https://pdfs.semanticscholar.org/cb94/e3d981a5e1901793c6bfedd93ce9cc07885d.pdf)
