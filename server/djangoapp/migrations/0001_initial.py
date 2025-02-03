from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('set', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('card_type', models.CharField(max_length=255)),
                ('bodyType', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=4)),
                ('image_url', models.URLField(max_length=200)),
            ],
        ),
    ]