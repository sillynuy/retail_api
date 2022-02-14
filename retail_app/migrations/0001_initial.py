# Generated by Django 4.0.2 on 2022-02-11 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Remain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remain2p', to='retail_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=40)),
                ('products', models.ManyToManyField(through='retail_app.Remain', to='retail_app.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('product', models.ManyToManyField(to='retail_app.Product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail_app.store')),
            ],
        ),
        migrations.AddField(
            model_name='remain',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remain2s', to='retail_app.store'),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('product', models.ManyToManyField(to='retail_app.Product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail_app.store')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='remain',
            unique_together={('store', 'product')},
        ),
    ]