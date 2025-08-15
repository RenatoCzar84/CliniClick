{% extends "base/base.html" %}
{% block title %}{% if edicao %}Editar Consulta{% else %}Agendar Consulta{% endif %} | Cliniclick{% endblock %}

{% block content %}
<div class="py-3">
  <div class="mb-2">
  <a class="btn btn-sm btn-outline-secondary" href="{% url 'usuarios:painel_usuario' %}">
    <i class="bi bi-arrow-left"></i> Voltar ao painel
  </a>
</div>
  <div class="card shadow-sm mx-auto" style="max-width:560px;">
    <div class="card-header bg-primary text-white text-center py-3">
      <strong class="fancy-title mb-0 fs-5">{% if edicao %}Editar Consulta{% else %}Agendar Consulta{% endif %}</strong>
    </div>
    <div class="card-body">
      <form method="post" novalidate>
        {% csrf_token %}

        <div class="mb-3">
          <label class="form-label">Especialidade</label>
          {{ form.especialidade }}
          <div class="invalid-feedback d-block">{{ form.especialidade.errors|striptags }}</div>
        </div>

        <div class="mb-3">
          <label class="form-label">Médico</label>
          {{ form.medico }}
          <div class="invalid-feedback d-block">{{ form.medico.errors|striptags }}</div>
        </div>

        <div class="row g-3">
          <div class="col-6">
            <label class="form-label">Data</label>
            {{ form.data }}
            <div class="invalid-feedback d-block">{{ form.data.errors|striptags }}</div>
          </div>
          <div class="col-6">
            <label class="form-label">Horário</label>
            {{ form.hora }}
            <div class="invalid-feedback d-block">{{ form.hora.errors|striptags }}</div>
          </div>
        </div>

        <div class="mb-3 mt-3">
          <label class="form-label">Observações (opcional)</label>
          {{ form.observacoes }}
          <div class="invalid-feedback d-block">{{ form.observacoes.errors|striptags }}</div>
        </div>

        <div class="d-flex gap-2">
          <button class="btn btn-primary" type="submit">{% if edicao %}Salvar{% else %}Agendar{% endif %}</button>
          <a class="btn btn-outline-secondary" href="{% url 'usuarios:painel_usuario' %}">Cancelar</a>
        </div>
      </form>
    </div>
  </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
(function(){
  const esp = document.getElementById('id_especialidade');
  const med = document.getElementById('id_medico');
  if (esp && med){
    async function loadMedicos(especialidadeId){
      if(!especialidadeId){ med.innerHTML = '<option value="">— selecione —</option>'; return; }
      med.disabled = true;
      const url = "{% url 'agenda:medicos_por_especialidade' 0 %}".replace('/0/', `/${especialidadeId}/`);
      try{
        const r = await fetch(url, {credentials:'same-origin'});
        const data = await r.json();
        med.innerHTML = '<option value="">— selecione —</option>' + data.medicos.map(m=>`<option value="${m.id}">${m.nome}</option>`).join('');
      }catch(e){
        med.innerHTML = '<option value="">(erro ao carregar)</option>';
      }finally{
        med.disabled = false;
      }
    }
    esp.addEventListener('change', e => loadMedicos(e.target.value));
    if (esp.value && (!med.value || med.options.length <= 1)) loadMedicos(esp.value);
  }
})();
</script>
{% endblock %}
