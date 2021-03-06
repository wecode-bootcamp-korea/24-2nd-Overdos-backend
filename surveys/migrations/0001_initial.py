# Generated by Django 3.2.7 on 2021-09-29 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'bodies',
            },
        ),
        migrations.CreateModel(
            name='Product_Symptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'db_table': 'product_symptoms',
            },
        ),
        migrations.CreateModel(
            name='SurveyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gender', models.CharField(choices=[('male', '남자'), ('female', '여자')], max_length=50)),
                ('age', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'surveyinfos',
            },
        ),
        migrations.CreateModel(
            name='SurveyInfo_Symptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surveyinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.surveyinfo')),
            ],
            options={
                'db_table': 'surveyinfo_symptoms',
            },
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('body', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.body')),
                ('product', models.ManyToManyField(through='surveys.Product_Symptom', to='products.Product')),
                ('surveyinfo', models.ManyToManyField(through='surveys.SurveyInfo_Symptom', to='surveys.SurveyInfo')),
            ],
            options={
                'db_table': 'symptoms',
            },
        ),
        migrations.AddField(
            model_name='surveyinfo_symptom',
            name='symptom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.symptom'),
        ),
        migrations.AddField(
            model_name='product_symptom',
            name='symptom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.symptom'),
        ),
    ]
