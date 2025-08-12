from django.db import migrations, models

def saneia_nulls(apps, schema_editor):
    # Troca NULL por '' nos campos que hoje são NOT NULL no schema
    # (use execute porque estamos antes da recriação da tabela)
    schema_editor.execute("UPDATE usuarios_usuario SET cep='' WHERE cep IS NULL;")
    schema_editor.execute("UPDATE usuarios_usuario SET rua='' WHERE rua IS NULL;")
    schema_editor.execute("UPDATE usuarios_usuario SET bairro='' WHERE bairro IS NULL;")
    schema_editor.execute("UPDATE usuarios_usuario SET cidade='' WHERE cidade IS NULL;")
    schema_editor.execute("UPDATE usuarios_usuario SET estado='' WHERE estado IS NULL;")
    schema_editor.execute("UPDATE usuarios_usuario SET telefone='' WHERE telefone IS NULL;")
    schema_editor.execute("UPDATE usuarios_usuario SET cpf='73197612874' WHERE cpf IS NULL;")
    schema_editor.execute("UPDATE usuarios_usuario SET plano_saude='' WHERE plano_saude IS NULL;")

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_rename_logradouro_usuario_rua'),  # deixe exatamente como já estava aí
    ]

    operations = [
        migrations.RunPython(saneia_nulls),
        migrations.AddField(
            model_name='usuario',
            name='complemento',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='usuario',
            name='numero',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
