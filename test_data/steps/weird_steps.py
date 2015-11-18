from romaine.steps import Given, When, Then, Step, And


@Given('When step_1')
def step_1():
    pass


@When('Then step_2')
def step_2():
    pass


@Then('And step_3')
def step_3():
    pass


@And('step_4')
def step_4():
    pass


@Step('step_5')
def step_5():
    pass


@Given('Givenness step_6')
def step_6():
    pass


@When('Whence step_7')
def step_7():
    pass


@Then('Thenceforth step_8')
def step_8():
    pass


@And('Android step_9')
def step_9():
    pass
