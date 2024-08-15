from django import forms
from .models import Customer, Invoice, InvoiceItem
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms import inlineformset_factory

class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'email', 'phone', 'customer_type', 'status']

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'unit_price']

InvoiceItemFormSet = inlineformset_factory(
    Invoice, InvoiceItem, form=InvoiceItemForm, extra=1, can_delete=True
)

class CreateInvoiceForm(forms.ModelForm):
    recipient_choice = forms.ChoiceField(
        choices=(('customer', 'Customer'), ('user', 'User')), 
        widget=forms.RadioSelect, 
        label="Send To"
    )
    recipient_user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False)

    class Meta:
        model = Invoice
        fields = ['due_date', 'recipient_choice', 'customer', 'recipient_user', 'discount', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'discount': forms.NumberInput(attrs={'step': '0.01'})
        }
    def clean(self):
        cleaned_data = super().clean()
        recipient_choice = cleaned_data.get("recipient_choice")
        
        if recipient_choice == 'customer' and not cleaned_data.get('customer'):
            self.add_error('customer', 'Please select a customer.')
        elif recipient_choice == 'user' and not cleaned_data.get('recipient_user'):
            self.add_error('recipient_user', 'Please select a user.')

        return cleaned_data
    def clean_due_date(self):
        invoice_date = timezone.now().date()
        due_date = self.cleaned_data.get('due_date')

        if due_date and due_date < invoice_date:
            raise ValidationError("Due date cannot be earlier than today.")
        return due_date

class UpdateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'email', 'phone', 'customer_type', 'status']

class UpdateInvoiceForm(forms.ModelForm):
    recipient_choice = forms.ChoiceField(
        choices=(('customer', 'Customer'), ('user', 'User')), 
        widget=forms.RadioSelect, 
        label="Send To"
    )
    recipient_user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False)

    class Meta:
        model = Invoice
        fields = ['due_date', 'recipient_choice', 'customer', 'recipient_user', 'discount', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'discount': forms.NumberInput(attrs={'step': '0.01'})
        }

    def clean(self):
        cleaned_data = super().clean()
        recipient_choice = cleaned_data.get("recipient_choice")
        
        if recipient_choice == 'customer' and not cleaned_data.get('customer'):
            self.add_error('customer', 'Please select a customer.')
        elif recipient_choice == 'user' and not cleaned_data.get('recipient_user'):
            self.add_error('recipient_user', 'Please select a user.')

        return cleaned_data

    def clean_due_date(self):
        invoice_date = timezone.now().date()
        due_date = self.cleaned_data.get('due_date')

        if due_date and due_date < invoice_date:
            raise ValidationError("Due date cannot be earlier than today.")
        return due_date
