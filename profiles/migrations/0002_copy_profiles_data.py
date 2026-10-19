from django.db import migrations


def copy_profiles_data(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    OldProfile = apps.get_model("oc_lettings_site", "Profile")
    NewProfile = apps.get_model("profiles", "Profile")

    for old_profile in OldProfile.objects.using(db_alias).order_by("pk"):
        NewProfile.objects.using(db_alias).create(
            pk=old_profile.pk,
            user_id=old_profile.user_id,
            favorite_city=old_profile.favorite_city,
        )


def reverse_profiles_data(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    OldProfile = apps.get_model("oc_lettings_site", "Profile")
    NewProfile = apps.get_model("profiles", "Profile")

    NewProfile.objects.using(db_alias).filter(
        pk__in=OldProfile.objects.using(db_alias).values_list("pk", flat=True)
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("oc_lettings_site", "0001_initial"),
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(copy_profiles_data, reverse_profiles_data),
    ]
