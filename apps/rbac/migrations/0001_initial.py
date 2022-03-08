# Generated by Django 3.1.13 on 2021-11-19 08:29

from django.conf import settings
import django.contrib.auth.models
import django.contrib.contenttypes.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('orgs', '0010_auto_20210219_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuPermission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Menu permission',
                'permissions': [('view_consoleview', 'Can view console view'), ('view_auditview', 'Can view audit view'), ('view_workspaceview', 'Can view workspace view')],
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=32, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=32, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('scope', models.CharField(choices=[('system', 'System'), ('org', 'Organization')], default='system', max_length=128, verbose_name='Scope')),
                ('builtin', models.BooleanField(default=False, verbose_name='Built-in')),
                ('comment', models.TextField(blank=True, default='', max_length=128, verbose_name='Comment')),
            ],
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('contenttypes.contenttype',),
            managers=[
                ('objects', django.contrib.contenttypes.models.ContentTypeManager()),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.permission',),
            managers=[
                ('objects', django.contrib.auth.models.PermissionManager()),
            ],
        ),
        migrations.CreateModel(
            name='RoleBinding',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=32, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=32, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('scope', models.CharField(choices=[('system', 'System'), ('org', 'Organization')], default='system', max_length=128, verbose_name='Scope')),
                ('org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role_bindings', to='orgs.organization', verbose_name='Organization')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_bindings', to='rbac.role', verbose_name='Role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_bindings', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Role binding',
                'unique_together': {('user', 'role', 'org')},
            },
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, related_name='roles', to='rbac.Permission', verbose_name='Permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('name', 'scope')},
        ),
        migrations.CreateModel(
            name='OrgRoleBinding',
            fields=[
            ],
            options={
                'verbose_name': 'Organization role binding',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('rbac.rolebinding',),
        ),
        migrations.CreateModel(
            name='SystemRoleBinding',
            fields=[
            ],
            options={
                'verbose_name': 'System role binding',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('rbac.rolebinding',),
        ),
        migrations.CreateModel(
            name='OrgRole',
            fields=[
            ],
            options={
                'verbose_name': 'Organization role',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('rbac.role',),
        ),
        migrations.CreateModel(
            name='SystemRole',
            fields=[
            ],
            options={
                'verbose_name': 'System role',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('rbac.role',),
        ),
    ]
