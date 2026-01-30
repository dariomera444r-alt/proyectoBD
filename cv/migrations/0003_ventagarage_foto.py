# Generated migration for adding foto field to VentaGarage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0002_alter_cursosrealizados_fechafin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventagarage',
            name='descripcion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='ventagarage',
            name='valordelbien',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='ventagarage',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='garage/productos/'),
        ),
        migrations.AlterModelOptions(
            name='ventagarage',
            options={'ordering': ['-idventagarage'], 'verbose_name': 'Producto en Venta', 'verbose_name_plural': 'Productos en Venta'},
        ),
    ]
