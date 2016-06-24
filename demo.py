import logging

from romaine.core import Core
from romaine.steps import Given, When, Then


def define_test_steps():

    @Given("I have a test framework")
    def i_have_a_test_framework():
        pass

    @When("I pass")
    def i_pass():
        pass

    @When("I fail")
    def i_fail():
        assert False

    @Then("everything's fine")
    def everything_is_fine():
        pass

    @Then("this step isn't run")
    def this_is_not_run():
        pass


FEATURE_LINES = [
    "Feature: Test framework",
    " As a conscientious developer",
    " I want to test my code",
    "",
    "  Scenario Outline: Outlined steps",
    "   Given I have a test framework",
    "    When I <action>",
    "    Then <result>",
    "",
    "Examples: Some examples",
    "| action | result              |",
    "| pass   | everything's fine   |",
    "| fail   | this step isn't run |",
    "",
    "  Scenario: Everything passes",
    "   Given I have a test framework",
    "    When I pass",
    "    Then everything's fine",
    "",
    "  Scenario: Something fails",
    "   Given I have a test framework",
    "    When I fail",
    "    Then this step isn't run",
]

if __name__ == "__main__":
    core = Core(log_level=logging.INFO)
    feature_parser = core.Parser().feature
    feature = feature_parser.get_feature(FEATURE_LINES)["feature"]
    define_test_steps()

    core.run_features(feature)
