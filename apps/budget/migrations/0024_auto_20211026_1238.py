# Generated by Django 3.0.8 on 2021-10-26 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0003_auto_20201204_1945'),
        ('budget', '0023_auto_20210811_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('group', models.CharField(choices=[('functional', 'Functional'), ('organic', 'Organic'), ('nature', 'Nature'), ('source', 'Source')], max_length=30, verbose_name='group')),
                ('type', models.CharField(choices=[('expense', 'Expense'), ('revenue', 'Revenue')], max_length=30, verbose_name='type')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
                'unique_together': {('name', 'group', 'type')},
            },
        ),
        migrations.AlterField(
            model_name='budget',
            name='output_file',
            field=models.FileField(blank=True, editable=False, help_text='Auto generated CSV file with all data from budget.', null=True, upload_to='exports', verbose_name='output file.'),
        ),
        migrations.CreateModel(
            name='CategoryMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, verbose_name='code')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_map', to='budget.Category', verbose_name='category')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_map', to='geo.Country', verbose_name='country')),
            ],
            options={
                'verbose_name': 'Category Mappping',
                'verbose_name_plural': 'Categories Mappping',
                'ordering': ['category', 'country'],
                'unique_together': {('code', 'country', 'category')},
            },
        ),
    ]
