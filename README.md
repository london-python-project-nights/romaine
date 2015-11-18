# romaine

[![Build Status](https://travis-ci.org/london-python-project-nights/romaine.png?branch=develop)](https://travis-ci.org/london-python-project-nights/romaine) [![Licence Status](https://img.shields.io/badge/licence-MIT-blue.svg)](https://github.com/london-python-project-nights/romaine) 

## Overview
`romaine` is a tool for running BDD style tests. Theses tests are written in Given-When-Then (a.k.a [Gherkin](https://cucumber.io/docs/reference#gherkin "Link to cucumber documentation")) syntax that enables users and developers to work together on features. `romaine` has been inspired by [lettuce][github_lettuce] but seeks to be more extensible and Python 3 friendly. Currently in an alpha stage, the intention is for `romaine` to become a complete tool for running these style of tests.

### Simple example

######calculator.feature
```gherkin
Feature: Addition
  Scenario: Add two numbers
    Given I have entered 50 into the calculator
    And I have entered 70 into the calculator
    When I press add
    Then the result should be 120 on the screen
```

######calculator_steps.py
```python
@Given('I have set 50 as the initial value')
def calculator_():
    calc = Calculator(50)

@When('I add 70 to the current value')
def calculator_add_70():
    calc.add(70)

@Then('the result should be 120 on the screen')
def calculator_value_120():
    assert 120 = calc.value
```
The feature file and the step definition file goes together. The user and developer will collaborate on the feature file and the developer will map the plain language feature file to the actual code, using the step definition file.

## Contributing

In order to run the tests for the project do the following:

``` bash
$ git clone git@github.com:london-python-project-nights/romaine.git
$ cd romaine
$ python setup.py test
```

## Requirements

* Python 3.2+
* Linux, Mac OS X (Should work on BSD, not tested on Windows)

## Licence

`romaine` is released under the [MIT License][mit_licence].

[github_lettuce]: https://github.com/gabrielfalcao/lettuce
[mit_licence]: https://github.com/london-python-project-nights/romaine/blob/develop/LICENSE
