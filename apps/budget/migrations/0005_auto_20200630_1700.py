# Generated by Django 3.0.5 on 2020-06-30 20:00

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0004_auto_20200629_0144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='budget',
            options={'verbose_name': 'budget', 'verbose_name_plural': 'budgets'},
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('budget_investment', models.FloatField(blank=True, null=True, verbose_name='initial budget for investment')),
                ('budget_operation', models.FloatField(blank=True, null=True, verbose_name='initial budget for operation')),
                ('budget_aggregated', models.FloatField(blank=True, null=True, verbose_name='initial budget')),
                ('execution_investment', models.FloatField(blank=True, null=True, verbose_name='execution for investment')),
                ('execution_operation', models.FloatField(blank=True, null=True, verbose_name='execution for operation')),
                ('execution_aggregated', models.FloatField(blank=True, null=True, verbose_name='execution')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='last update')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.Budget', verbose_name='budget')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='budget.Function', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'function',
                'verbose_name_plural': 'functions',
            },
        ),
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('budget_investment', models.FloatField(blank=True, null=True, verbose_name='initial budget for investment')),
                ('budget_operation', models.FloatField(blank=True, null=True, verbose_name='initial budget for operation')),
                ('budget_aggregated', models.FloatField(blank=True, null=True, verbose_name='initial budget')),
                ('execution_investment', models.FloatField(blank=True, null=True, verbose_name='execution for investment')),
                ('execution_operation', models.FloatField(blank=True, null=True, verbose_name='execution for operation')),
                ('execution_aggregated', models.FloatField(blank=True, null=True, verbose_name='execution')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='last update')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.Budget', verbose_name='budget')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='budget.Agency', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'agency',
                'verbose_name_plural': 'agencies',
            },
        ),
    ]
