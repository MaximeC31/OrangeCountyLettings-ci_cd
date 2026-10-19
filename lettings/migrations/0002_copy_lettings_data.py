from django.db import migrations


def copy_lettings_data(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    OldAddress = apps.get_model("oc_lettings_site", "Address")
    OldLetting = apps.get_model("oc_lettings_site", "Letting")
    NewAddress = apps.get_model("lettings", "Address")
    NewLetting = apps.get_model("lettings", "Letting")

    for old_address in OldAddress.objects.using(db_alias).order_by("pk"):
        NewAddress.objects.using(db_alias).create(
            pk=old_address.pk,
            number=old_address.number,
            street=old_address.street,
            city=old_address.city,
            state=old_address.state,
            zip_code=old_address.zip_code,
            country_iso_code=old_address.country_iso_code,
        )

    for old_letting in OldLetting.objects.using(db_alias).order_by("pk"):
        NewLetting.objects.using(db_alias).create(
            pk=old_letting.pk,
            title=old_letting.title,
            address_id=old_letting.address_id,
        )


def reverse_lettings_data(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    OldAddress = apps.get_model("oc_lettings_site", "Address")
    OldLetting = apps.get_model("oc_lettings_site", "Letting")
    NewAddress = apps.get_model("lettings", "Address")
    NewLetting = apps.get_model("lettings", "Letting")

    NewLetting.objects.using(db_alias).filter(
        pk__in=OldLetting.objects.using(db_alias).values_list("pk", flat=True)
    ).delete()
    NewAddress.objects.using(db_alias).filter(
        pk__in=OldAddress.objects.using(db_alias).values_list("pk", flat=True)
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("oc_lettings_site", "0001_initial"),
        ("lettings", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(copy_lettings_data, reverse_lettings_data),
    ]
