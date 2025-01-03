# Generated by Django 5.1.4 on 2024-12-10 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sklep', '0004_alter_product_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'ordering': ['surname'], 'permissions': [('can_view_other_persons', 'Can view other persons')]},
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='Product',
            new_name='product',
        ),
    ]
