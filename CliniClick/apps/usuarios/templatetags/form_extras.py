from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    """
    Adiciona classes CSS ao widget do campo sem perder as já existentes.
    Uso: {{ field|add_class:"form-control" }}
    """
    existing = field.field.widget.attrs.get("class", "")
    new = (existing + " " + css).strip()
    return field.as_widget(attrs={**field.field.widget.attrs, "class": new})
