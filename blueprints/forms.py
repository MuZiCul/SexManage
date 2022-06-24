import wtforms

from wtforms.validators import length


class LoginForm(wtforms.Form):
    account = wtforms.StringField(validators=[length(min=2, max=254)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    captcha = wtforms.StringField(validators=[length(min=0, max=10)])

    def validate_account(self, field):
        data = field.data
        if len(data) < 1:
            raise wtforms.ValidationError('用户名不能为空！')

    def validate_password(self, field):
        data = field.data
        if len(data) < 1:
            raise wtforms.ValidationError('密码不能为空！')

    def validate_captcha(self, field):
        data = field.data
        if len(data) != 6:
            raise wtforms.ValidationError('验证码不正确！')
