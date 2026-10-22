"""Transfer historical addresses and lettings to the lettings app."""

from django.db import migrations


def copy_lettings_data(apps, schema_editor):
    """Copy addresses, then lettings, keeping their IDs and relationships."""
    database_alias = schema_editor.connection.alias

    SourceAddress = apps.get_model("oc_lettings_site", "Address")
    SourceLetting = apps.get_model("oc_lettings_site", "Letting")
    TargetAddress = apps.get_model("lettings", "Address")
    TargetLetting = apps.get_model("lettings", "Letting")

    for address in SourceAddress.objects.using(database_alias).order_by("pk"):
        TargetAddress.objects.using(database_alias).create(
            pk=address.pk,
            number=address.number,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            country_iso_code=address.country_iso_code,
        )

    for letting in SourceLetting.objects.using(database_alias).order_by("pk"):
        TargetLetting.objects.using(database_alias).create(
            pk=letting.pk,
            title=letting.title,
            address_id=letting.address_id,
        )


def reverse_lettings_data(apps, schema_editor):
    """Delete matching target rows; this does not restore historical data."""
    database_alias = schema_editor.connection.alias

    SourceAddress = apps.get_model("oc_lettings_site", "Address")
    SourceLetting = apps.get_model("oc_lettings_site", "Letting")
    TargetAddress = apps.get_model("lettings", "Address")
    TargetLetting = apps.get_model("lettings", "Letting")

    source_letting_ids = SourceLetting.objects.using(database_alias).values_list("pk", flat=True)
    TargetLetting.objects.using(database_alias).filter(pk__in=source_letting_ids).delete()

    source_address_ids = SourceAddress.objects.using(database_alias).values_list("pk", flat=True)
    TargetAddress.objects.using(database_alias).filter(pk__in=source_address_ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("oc_lettings_site", "0001_initial"),
        ("lettings", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(copy_lettings_data, reverse_lettings_data),
    ]
