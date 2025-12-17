from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_rename_user_id_userprofile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user_addresses",
                to="misc.address",
            ),
        ),
    ]
