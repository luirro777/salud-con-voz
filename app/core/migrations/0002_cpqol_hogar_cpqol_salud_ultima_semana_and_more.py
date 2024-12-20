# Generated by Django 5.0.8 on 2024-11-08 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpqol',
            name='hogar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.hogar'),
        ),
        migrations.AddField(
            model_name='cpqol',
            name='salud_ultima_semana',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.saludultimasemana'),
        ),
        migrations.AddField(
            model_name='cpqol',
            name='salud_ultima_semana_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.saludultimasemana2'),
        ),
        migrations.AlterField(
            model_name='saludultimasemana2',
            name='atencion',
            field=models.CharField(choices=[('Mucho', 'Mucho'), ('Muchísimo', 'Muchísimo'), ('Un poco', 'Un poco'), ('Nada', 'Nada'), ('Moderadamente', 'Moderadamente')], max_length=100, verbose_name='¿El chico/a pudo prestar atención en clase?'),
        ),
        migrations.AlterField(
            model_name='saludultimasemana2',
            name='colegio',
            field=models.CharField(choices=[('Mucho', 'Mucho'), ('Muchísimo', 'Muchísimo'), ('Un poco', 'Un poco'), ('Nada', 'Nada'), ('Moderadamente', 'Moderadamente')], max_length=100, verbose_name='¿Al chico/a le fue bien en la escuela o en el colegio?'),
        ),
        migrations.AlterField(
            model_name='saludultimasemana2',
            name='cosas_queria',
            field=models.CharField(choices=[('Mucho', 'Mucho'), ('Muchísimo', 'Muchísimo'), ('Un poco', 'Un poco'), ('Nada', 'Nada'), ('Moderadamente', 'Moderadamente')], max_length=100, verbose_name='¿El chico/a hizo las cosas que quería hacer en su tiempo libre?'),
        ),
        migrations.AlterField(
            model_name='saludultimasemana2',
            name='diversion',
            field=models.CharField(choices=[('Mucho', 'Mucho'), ('Muchísimo', 'Muchísimo'), ('Un poco', 'Un poco'), ('Nada', 'Nada'), ('Moderadamente', 'Moderadamente')], max_length=100, verbose_name='¿El chico/a se divirtió con sus amigos/as?'),
        ),
        migrations.AlterField(
            model_name='saludultimasemana2',
            name='energia',
            field=models.CharField(choices=[('Mucho', 'Mucho'), ('Muchísimo', 'Muchísimo'), ('Un poco', 'Un poco'), ('Nada', 'Nada'), ('Moderadamente', 'Moderadamente')], max_length=100, verbose_name='¿El chico/a se sintió lleno/a de energía?'),
        ),
        migrations.AlterField(
            model_name='saludultimasemana2',
            name='fisicamente',
            field=models.CharField(choices=[('Mucho', 'Mucho'), ('Muchísimo', 'Muchísimo'), ('Un poco', 'Un poco'), ('Nada', 'Nada'), ('Moderadamente', 'Moderadamente')], max_length=100, verbose_name='¿El chico/a se sintió bien y físicamente en forma?'),
        ),
        migrations.AlterField(
            model_name='saludultimasemana2',
            name='justicia',
            field=models.CharField(choices=[('Mucho', 'Mucho'), ('Muchísimo', 'Muchísimo'), ('Un poco', 'Un poco'), ('Nada', 'Nada'), ('Moderadamente', 'Moderadamente')], max_length=100, verbose_name='¿Los padres del chico/a fueron justos con él/ella?'),
        ),
        migrations.AlterField(
            model_name='saludultimasemana2',
            name='soledad',
            field=models.CharField(choices=[('Mucho', 'Mucho'), ('Muchísimo', 'Muchísimo'), ('Un poco', 'Un poco'), ('Nada', 'Nada'), ('Moderadamente', 'Moderadamente')], max_length=100, verbose_name='¿El chico/a se sintió solo/a?'),
        ),
        migrations.AlterField(
            model_name='saludultimasemana2',
            name='tiempo_libre',
            field=models.CharField(choices=[('Mucho', 'Mucho'), ('Muchísimo', 'Muchísimo'), ('Un poco', 'Un poco'), ('Nada', 'Nada'), ('Moderadamente', 'Moderadamente')], max_length=100, verbose_name='¿El chico/a tuvo suficiente tiempo para él/ella?'),
        ),
        migrations.AlterField(
            model_name='saludultimasemana2',
            name='tristeza',
            field=models.CharField(choices=[('Mucho', 'Mucho'), ('Muchísimo', 'Muchísimo'), ('Un poco', 'Un poco'), ('Nada', 'Nada'), ('Moderadamente', 'Moderadamente')], max_length=100, verbose_name='¿El chico/a se sintió triste?'),
        ),
    ]
