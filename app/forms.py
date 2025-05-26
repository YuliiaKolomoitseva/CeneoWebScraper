from wtforms import Form, StringField, SubmitField, validators

class ExtractForm(Form):
    product_id = StringField("Product id", name="product_id", id="product_id", validators=[validators.DataRequired(),
validators.length(min=6, max=10, message="Product id should have between 6 and 10 characters"),validators.Regexp(r'[0-9]{6,10}*', message="Product id can contain only digits")
])

    submit = SubmitField("Extract opinions")