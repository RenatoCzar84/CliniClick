# apps/agenda/forms.py
from datetime import datetime, time as time_cls
from django import forms
from django.utils import timezone
from .models import Agendamento, Especialidade, Medico, ExameTipo


def _slot_choices():
    """Gera slots de 30 em 30 min das 08:00 às 17:30 (último início 17:30)."""
    slots = []
    h, m = 8, 0
    while True:
        slots.append(f"{h:02d}:{m:02d}")
        m += 30
        if m >= 60:
            m = 0
            h += 1
        if h == 18 and m == 0:
            break
    return [(s, s) for s in slots]


class AgendarConsultaForm(forms.ModelForm):
    # Data só via calendário + hora em slots de 30 em 30 (08:00–17:30)
    data = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "id": "id_data",
                "inputmode": "none",
                "onkeydown": "return false;",
                "onpaste": "return false;",
                "onbeforeinput": "return false;",
            }
        )
    )
    hora = forms.ChoiceField(
        choices=_slot_choices(),
        widget=forms.Select(attrs={"class": "form-select", "id": "id_hora"})
    )

    class Meta:
        model = Agendamento
        # data_hora será montado no save() a partir de data + hora
        fields = ["especialidade", "medico", "observacoes"]
        widgets = {
            "especialidade": forms.Select(attrs={"class": "form-select", "id": "id_especialidade"}),
            "medico": forms.Select(attrs={"class": "form-select", "id": "id_medico"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["especialidade"].queryset = Especialidade.objects.all()
        self.fields["medico"].queryset = Medico.objects.filter(ativo=True)

        # data mínima = hoje
        self.fields["data"].widget.attrs["min"] = timezone.localdate().isoformat()

        # edição: preencher data/hora a partir de data_hora existente
        if self.instance and self.instance.pk and self.instance.data_hora:
            dtz = timezone.localtime(self.instance.data_hora)
            self.initial.setdefault("data", dtz.date())
            self.initial.setdefault("hora", dtz.strftime("%H:%M"))

        # filtra médicos conforme especialidade selecionada
        esp = self.data.get("especialidade") or self.initial.get("especialidade")
        if esp:
            try:
                self.fields["medico"].queryset = Medico.objects.filter(
                    ativo=True, especialidade_id=int(esp)
                )
            except (TypeError, ValueError):
                pass

    def clean(self):
        from datetime import datetime as _dt
        cleaned = super().clean()
        d = cleaned.get("data")
        h = cleaned.get("hora")
        med = cleaned.get("medico")

        if d and h:
            hh, mm = map(int, h.split(":"))
            naive = _dt.combine(d, time_cls(hh, mm))
            aware = timezone.make_aware(naive, timezone.get_current_timezone())
            if aware <= timezone.now():
                self.add_error("data", "Escolha uma data/horário no futuro.")
            cleaned["data_hora_combined"] = aware

        # conflito com médico
        if med and cleaned.get("data_hora_combined"):
            conflict = Agendamento.objects.filter(
                tipo=Agendamento.TIPO_CONSULTA,
                medico=med,
                data_hora=cleaned["data_hora_combined"],
            )
            if self.instance and self.instance.pk:
                conflict = conflict.exclude(pk=self.instance.pk)
            if conflict.exists():
                self.add_error("data", "Este médico já possui consulta nesse horário.")
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.tipo = Agendamento.TIPO_CONSULTA
        obj.data_hora = self.cleaned_data.get("data_hora_combined")
        if commit:
            obj.save()
        return obj


class AgendarExameForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "id": "id_data",
                "inputmode": "none",
                "onkeydown": "return false;",
                "onpaste": "return false;",
                "onbeforeinput": "return false;",
            }
        )
    )
    hora = forms.ChoiceField(
        choices=_slot_choices(),
        widget=forms.Select(attrs={"class": "form-select", "id": "id_hora"})
    )

    class Meta:
        model = Agendamento
        fields = ["exame_tipo", "observacoes"]
        widgets = {
            "exame_tipo": forms.Select(attrs={"class": "form-select", "id": "id_exame_tipo"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["exame_tipo"].queryset = ExameTipo.objects.filter(ativo=True)

        # data mínima = hoje
        self.fields["data"].widget.attrs["min"] = timezone.localdate().isoformat()

        # edição: preencher data/hora a partir de data_hora existente
        if self.instance and self.instance.pk and self.instance.data_hora:
            dtz = timezone.localtime(self.instance.data_hora)
            self.initial.setdefault("data", dtz.date())
            self.initial.setdefault("hora", dtz.strftime("%H:%M"))

    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("data")
        h = cleaned.get("hora")
        if d and h:
            hh, mm = map(int, h.split(":"))
            naive = datetime.combine(d, time_cls(hh, mm))
            aware = timezone.make_aware(naive, timezone.get_current_timezone())
            if aware <= timezone.now():
                self.add_error("data", "Escolha uma data/horário no futuro.")
            cleaned["data_hora_combined"] = aware
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.tipo = Agendamento.TIPO_EXAME
        obj.data_hora = self.cleaned_data.get("data_hora_combined")
        if commit:
            obj.save()
        return obj
