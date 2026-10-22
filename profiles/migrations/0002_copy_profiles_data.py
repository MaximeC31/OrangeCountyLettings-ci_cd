"""Transfer historical profiles to the profiles app."""

from django.db import migrations


def copy_profiles_data(apps, schema_editor):
    """Copy profiles, keeping their IDs, user links and favorite cities."""
    database_alias = schema_editor.connection.alias

    SourceProfile = apps.get_model("oc_lettings_site", "Profile")
    TargetProfile = apps.get_model("profiles", "Profile")

    for profile in SourceProfile.objects.using(database_alias).order_by("pk"):
        TargetProfile.objects.using(database_alias).create(
            pk=profile.pk,
            user_id=profile.user_id,
            favorite_city=profile.favorite_city,
        )


def reverse_profiles_data(apps, schema_editor):
    """Delete matching target profiles; this does not restore historical data."""
    database_alias = schema_editor.connection.alias

    SourceProfile = apps.get_model("oc_lettings_site", "Profile")
    TargetProfile = apps.get_model("profiles", "Profile")

    source_profile_ids = SourceProfile.objects.using(database_alias).values_list("pk", flat=True)
    TargetProfile.objects.using(database_alias).filter(pk__in=source_profile_ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("oc_lettings_site", "0001_initial"),
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(copy_profiles_data, reverse_profiles_data),
    ]
