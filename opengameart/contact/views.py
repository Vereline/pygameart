from django.shortcuts import render, redirect
from .forms import ContactForm
# Create your views here.


def contacts_page(request):
    form = ContactForm()
    return render(request, 'contacts.html', {'contact_form': form})


def apply_contact_form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            return redirect('about_page')
        else:
            form = ContactForm()
            return render(request, 'contacts.html', {'contact_form': form})
    else:
        form = ContactForm()
    return render(request, 'contacts.html', {'contact_form': form})
