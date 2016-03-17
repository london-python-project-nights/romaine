from romaine.steps import Given, When, Then


@Given('step_\d')
def given_n():
    pass


@When('step_(p?<p>:\d)')
def when_n(n):
    assert n


@Then('step(.+)')
def step_s(s):
    assert s
