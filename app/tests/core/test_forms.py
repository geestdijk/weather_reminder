from core.forms import SignUpForm


def test_signup_form():
    data = {'email': 'some_email',
            'name': 'some_name',
            'password1': 'password',
            'password2': 'password'}
    form = SignUpForm(data=data)
    assert form.is_valid()
