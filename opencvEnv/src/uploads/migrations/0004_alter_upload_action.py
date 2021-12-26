# Generated by Django 3.2.9 on 2021-12-26 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0003_alter_upload_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='action',
            field=models.CharField(choices=[('NO_FILTER', 'no filter'), ('COLORIZED', 'colorized'), ('GRAYSCALE', 'grayscale'), ('BLURRED', 'blurred'), ('BINARY', 'binary'), ('INVERT', 'invert'), ('CARTOONISED', 'cartoonised'), ('WATER-ART', 'water-art'), ('SHARPEN', 'sharpen'), ('SEPIA', 'sepia'), ('EMBOSS', 'emboss'), ('WARM', 'warm'), ('COOL', 'cool'), ('SKETCH', 'sketch'), ('HDR', 'hdr')], default='NO_FILTER', max_length=50),
        ),
    ]