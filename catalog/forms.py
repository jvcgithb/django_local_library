from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.
#
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
#from .forms import ReneweBookForm
from django.contrib.auth.decorators import permission_required

from django.forms import ModelForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class RenewBookForm(forms.Form):
    """
    Formulario para un bibliotecario para renovar libros.
    """
    renewal_date = forms.DateField(help_text="Ingrese una fecha entre ahora y 4 semanas (predeterminado 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Verifica que la fecha no está en el pasado.
        if data < datetime.date.today():
            raise ValidationError(_('Fecha inválida - renovación en el pasado'))
        #Veridica que la fecha está dentro del rango El bibliotecario puede cambiar (+4 semanas)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Fecha inválida - renovación con más de 4 semanas de antelación'))

        # Recuerde devolver siempre los datos limpios.
        return data
    
    #def clean_due_back(self):
    #    data = self.cleaned_data['due_back']
    #    if data < datetime.date.today():
    #        raise ValidationError(_('Invalid date - renewal in past'))
        
    #    if data > datetime.date.today() + datetime.timedelta(weeks=4):
    #        raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

    #    return data


    class Meta:
        model = BookInstance
        fields = ['due_back',]
        labels = { 'due_back': _('Renewal date'), }
        help_texts = { 'due_back': _('Enter a date between now and 4 weeks (default 3).'), }

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
