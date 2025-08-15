from django.db import migrations

def seed_forward(apps, schema_editor):
    Especialidade = apps.get_model("agenda", "Especialidade")
    Medico = apps.get_model("agenda", "Medico")
    ExameTipo = apps.get_model("agenda", "ExameTipo")

    # 5 especialidades com 5 médicos cada
    mapa = {
        "Cardiologia": [
            "Dra. Ana Souza",
            "Dr. Bruno Lima",
            "Dr. Carlos Menezes",
            "Dra. Daniela Prado",
            "Dr. Eduardo Martins",
        ],
        "Clínica Geral": [
            "Dr. Felipe Rocha",
            "Dra. Gabriela Nunes",
            "Dr. Henrique Alves",
            "Dra. Isabela Castro",
            "Dr. João Pedro Santos",
        ],
        "Dermatologia": [
            "Dra. Karina Duarte",
            "Dr. Leonardo Pires",
            "Dra. Mariana Araújo",
            "Dr. Nelson Barros",
            "Dra. Olivia Teixeira",
        ],
        "Ortopedia": [
            "Dr. Paulo Viana",
            "Dra. Renata Campos",
            "Dr. Renato Freitas",
            "Dra. Sabrina Lopes",
            "Dr. Tiago Ribeiro",
        ],
        "Pediatria": [
            "Dra. Vanessa Maia",
            "Dr. Wagner Costa",
            "Dra. Bianca Pereira",
            "Dr. Yuri Lopes",
            "Dra. Zilda Monteiro",
        ],
    }

    exames = [
        "Hemograma",
        "Glicemia",
        "Colesterol Total",
        "Triglicerídeos",
        "TSH",
        "T3 Livre",
        "T4 Livre",
        "Urina Tipo 1",
        "Urocultura",
        "Raio-X",
        "Ultrassom",
        "Eletrocardiograma (ECG)",
        "Ecocardiograma",
        "Tomografia Computadorizada",
        "Ressonância Magnética",
    ]

    # Cria especialidades e médicos
    for esp_nome, medicos in mapa.items():
        esp, _ = Especialidade.objects.get_or_create(nome=esp_nome)
        for nome_med in medicos:
            Medico.objects.get_or_create(
                nome=nome_med,
                especialidade=esp,
                defaults={"ativo": True},
            )

    # Cria tipos de exame
    for ex in exames:
        ExameTipo.objects.get_or_create(nome=ex, defaults={"ativo": True})

def seed_backward(apps, schema_editor):
    # rollback opcional: remove APENAS os dados semeados acima
    Especialidade = apps.get_model("agenda", "Especialidade")
    Medico = apps.get_model("agenda", "Medico")
    ExameTipo = apps.get_model("agenda", "ExameTipo")

    mapa = {
        "Cardiologia": [
            "Dra. Ana Souza",
            "Dr. Bruno Lima",
            "Dr. Carlos Menezes",
            "Dra. Daniela Prado",
            "Dr. Eduardo Martins",
        ],
        "Clínica Geral": [
            "Dr. Felipe Rocha",
            "Dra. Gabriela Nunes",
            "Dr. Henrique Alves",
            "Dra. Isabela Castro",
            "Dr. João Pedro Santos",
        ],
        "Dermatologia": [
            "Dra. Karina Duarte",
            "Dr. Leonardo Pires",
            "Dra. Mariana Araújo",
            "Dr. Nelson Barros",
            "Dra. Olivia Teixeira",
        ],
        "Ortopedia": [
            "Dr. Paulo Viana",
            "Dra. Renata Campos",
            "Dr. Renato Freitas",
            "Dra. Sabrina Lopes",
            "Dr. Tiago Ribeiro",
        ],
        "Pediatria": [
            "Dra. Vanessa Maia",
            "Dr. Wagner Costa",
            "Dra. Bianca Pereira",
            "Dr. Yuri Lopes",
            "Dra. Zilda Monteiro",
        ],
    }

    exames = [
        "Hemograma",
        "Glicemia",
        "Colesterol Total",
        "Triglicerídeos",
        "TSH",
        "T3 Livre",
        "T4 Livre",
        "Urina Tipo 1",
        "Urocultura",
        "Raio-X",
        "Ultrassom",
        "Eletrocardiograma (ECG)",
        "Ecocardiograma",
        "Tomografia Computadorizada",
        "Ressonância Magnética",
    ]

    # Remove exames semeados
    ExameTipo.objects.filter(nome__in=exames).delete()

    # Remove médicos e especialidades semeados
    for esp_nome, medicos in mapa.items():
        try:
            esp = Especialidade.objects.get(nome=esp_nome)
        except Especialidade.DoesNotExist:
            continue
        Medico.objects.filter(especialidade=esp, nome__in=medicos).delete()
        # tenta apagar a especialidade (só se não ficar médico associado)
        try:
            esp.delete()
        except Exception:
            pass

class Migration(migrations.Migration):

    dependencies = [
        ("agenda", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_backward),
    ]
