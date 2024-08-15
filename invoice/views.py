from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CreateCustomerForm, CreateInvoiceForm, InvoiceItemFormSet, UpdateCustomerForm, UpdateInvoiceForm
from django.urls import reverse_lazy
from .models import Customer, Invoice, InvoiceItem
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa

@login_required(login_url=reverse_lazy('user:login'))
def add_customer(request):

    form = CreateCustomerForm()

    if request.method == "POST":
        form = CreateCustomerForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(reverse_lazy('user:dashboard'))
    context = {'customer_form': form}
    return render(request, 'invoice/add_customer.html',context=context)

@login_required
def add_invoice(request):
    if request.method == 'POST':
        invoice_form = CreateInvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)

        if invoice_form.is_valid() and formset.is_valid():
            # First, save the invoice instance
            invoice = invoice_form.save(commit=False)
            invoice.sender = request.user
            invoice.save()

            # Now iterate over each form in the formset and link them to the invoice
            for form in formset:
                invoice_item = form.save(commit=False)
                invoice_item.invoice = invoice  # Assign the invoice to the item
                invoice_item.save()

            return redirect('invoice:view_user_invoices')
    else:
        invoice_form = CreateInvoiceForm()
        formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.none())

    context = {
        'invoice_form': invoice_form,
        'formset': formset,
    }

    return render(request, 'invoice/create_invoice.html', context)

@login_required(login_url=reverse_lazy('user:login'))
def view_customers(request):
    # Filter customer records based on the currently logged-in user
    print(request.user)
    customer_records = Customer.objects.filter(user=request.user)
    print(customer_records)
    context = {'customer_records':customer_records}
    return render(request, 'invoice/customer_list.html', context=context)  

@login_required(login_url=reverse_lazy('user:login'))
def view_invoices(request, customer_id):
    # Retrieve the customer object based on the customer_id
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    
    # Retrieve all invoices belonging to the specified customer
    invoices = Invoice.objects.filter(customer=customer)

    # Pass the customer and invoices to the template context
    context = {
        'customer': customer,
        'invoices': invoices,
    }

    # Render the template and pass the context
    return render(request, 'invoice/view_invoices.html', context)


@login_required(login_url=reverse_lazy('user:login'))
def view_user_invoices(request):
    user = request.user

    # Invoices sent by the user
    sent_invoices = Invoice.objects.filter(sender=user)

    # Invoices received by the user
    received_invoices = Invoice.objects.filter(recipient_user=user)

    context = {
        'sent_invoices': sent_invoices,
        'received_invoices': received_invoices
    }
    return render(request, 'invoice/user_invoices.html', context)

@login_required(login_url=reverse_lazy('user:login'))
def update_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    
    if request.method == 'POST':
        form = UpdateInvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('user:dashboard')
    else:
        form = UpdateInvoiceForm(instance=invoice)
    
    context = {'form': form}
    return render(request, 'invoice/update_invoice.html', context)

# Delete an invoice
@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, sender=request.user)
    
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, 'Invoice has been deleted successfully.')
        return redirect('invoice:user_invoices')  # Redirect to the invoices list view
    
    return render(request, 'invoice/confirm_delete.html', {'object': invoice, 'type': 'invoice'})
@login_required(login_url=reverse_lazy('user:login'))
def update_customer(request, pk):
    customer= Customer.objects.get(id=pk)
    form = UpdateCustomerForm(instance=customer)
    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('user:dashboard')
    context={'form':form}

    return render(request, 'invoice/update_customer.html', context=context)

# Delete a customer
@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
    
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer has been deleted successfully.')
        return redirect('invoice:customers')  # Redirect to the customer list view
    
    return render(request, 'confirm_delete.html', {'object': customer, 'type': 'customer'})

@login_required(login_url=reverse_lazy('user:login'))
def generate_receipt_pdf(request, invoice_number):
    # Retrieve the invoice data
    invoice = Invoice.objects.get(invoice_number=invoice_number)

    # Prepare the context to pass to the template
    context = {
        'invoice': invoice,
    }

    # Render the HTML template
    template = get_template('invoice/receipt_template.html')
    rendered_template = template.render(context)

    # Create a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="receipt_{invoice.invoice_number}.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(
        rendered_template, dest=response, encoding='utf-8')

    # If PDF generation failed
    if pisa_status.err:
        return HttpResponse('PDF generation error!')

    return response
def receipt(request):
    return render(request, 'invoice/receipt_template.html')