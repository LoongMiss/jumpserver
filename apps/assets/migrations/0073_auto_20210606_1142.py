# Generated by Django 3.1.6 on 2021-06-06 03:42

from django.utils import timezone
from django.db import migrations, models, transaction
import django.db.models.deletion


def migrate_system_assets_to_authbook(apps, schema_editor):
    system_user_model = apps.get_model("assets", "SystemUser")
    system_user_asset_model = system_user_model.assets.through
    authbook_model = apps.get_model('assets', 'AuthBook')
    history_model = apps.get_model("assets", "HistoricalAuthBook")

    print()
    system_users = system_user_model.objects.all()
    for s in system_users:
        while True:
            systemuser_asset_relations = system_user_asset_model.objects.filter(systemuser=s)[:20]
            if not systemuser_asset_relations:
                break
            authbooks = []
            relations_ids = []
            historys = []
            for i in systemuser_asset_relations:
                authbook = authbook_model(asset=i.asset, systemuser=i.systemuser, org_id=s.org_id)
                authbooks.append(authbook)
                relations_ids.append(i.id)

                history = history_model(
                    asset=i.asset, systemuser=i.systemuser,
                    date_created=timezone.now(), date_updated=timezone.now(),
                )
                history.history_type = '-'
                history.history_date = timezone.now()
                historys.append(history)

            with transaction.atomic():
                print("  Migrate system user assets relations: {} items".format(len(relations_ids)))
                authbook_model.objects.bulk_create(authbooks, ignore_conflicts=True)
                history_model.objects.bulk_create(historys)
                system_user_asset_model.objects.filter(id__in=relations_ids).delete()


def migrate_authbook_secret_to_system_user(apps, schema_editor):
    authbook_model = apps.get_model('assets', 'AuthBook')
    history_model = apps.get_model('assets', 'HistoricalAuthBook')

    print()
    authbooks_without_systemuser = authbook_model.objects.filter(systemuser__isnull=True)
    for authbook in authbooks_without_systemuser:
        matched = authbook_model.objects.filter(
            asset=authbook.asset, systemuser__username=authbook.username
        )
        if not matched:
            continue
        historys = []
        for i in matched:
            history = history_model(
                asset=i.asset, systemuser=i.systemuser,
                date_created=timezone.now(), date_updated=timezone.now(),
                version=authbook.version
            )
            history.history_type = '-'
            history.history_date = timezone.now()
            historys.append(history)

        with transaction.atomic():
            print("  Migrate secret to system user assets account: {} items".format(len(historys)))
            matched.update(password=authbook.password, private_key=authbook.private_key,
                           public_key=authbook.public_key, version=authbook.version)
            history_model.objects.bulk_create(historys)


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0072_historicalauthbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='authbook',
            name='systemuser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.systemuser', verbose_name='System user'),
        ),
        migrations.AddField(
            model_name='historicalauthbook',
            name='systemuser',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='assets.systemuser', verbose_name='System user'),
        ),
        migrations.AlterUniqueTogether(
            name='authbook',
            unique_together={('username', 'asset', 'systemuser')},
        ),
        migrations.RunPython(migrate_system_assets_to_authbook),
        migrations.RunPython(migrate_authbook_secret_to_system_user),
        migrations.RemoveField(
            model_name='authbook',
            name='is_latest',
        ),
        migrations.RemoveField(
            model_name='historicalauthbook',
            name='is_latest',
        ),
    ]