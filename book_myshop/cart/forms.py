from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, i) for i in range(1, 51)]


class CartAddProductForm(forms.Form):
    """Форма для изменения количество продуктов в корзине."""
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
