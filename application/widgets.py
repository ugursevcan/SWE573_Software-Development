from django import forms
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe

class LocationWidget(TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        return mark_safe(html + '''
            <script>
            // Initialize the map autocomplete
            function initAutocomplete() {
                var input = document.getElementById("id_location");
                var autocomplete = new google.maps.places.Autocomplete(input);
                autocomplete.setFields(["geometry"]);
            }
            </script>
            <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initAutocomplete" async defer></script>
        ''')
