from django.db                          import models, IntegrityError
from django.db.models.aggregates        import Max
from django.contrib.sessions.models     import Session
from django.contrib.auth.models         import User, Permission
from django.db.models                   import Avg
from django.contrib.auth                import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Ckeditor
from tinymce.models                 import HTMLField

# Signals
from django.db.models.signals       import pre_save, post_save
from django.dispatch                import receiver

# HTML Safe String  
from django.utils.safestring        import mark_safe

# Send mail Django's Inbuilt function
from django.core.mail               import send_mail
from django.template.loader         import render_to_string

# Json
import json

# Forms
from django                 import forms       

# Regex
import re

# Django Settings
from django.conf            import settings

# UUID
import uuid

# Django Validators
from django.core.validators import MaxValueValidator, MinValueValidator

# Urllib
import urllib.parse

# Timezone
from django.utils   import timezone

# JSON Editor
from jsoneditor.forms import JSONEditor

# Django Tenants
from django_tenants.models import TenantMixin, DomainMixin

# Django Tenant User
from tenant_users.tenants.models import TenantBase, UserProfile




# Object Permissions
class ObjectPermission(models.Model):
    user            =   models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission      =   models.ForeignKey(Permission, on_delete=models.CASCADE)
    object_id       =   models.PositiveIntegerField()
    content_type    =   models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'permission', 'object_id', 'content_type')

# Common Model
class CommonModel(models.Model):
    extra_params            =   models.JSONField        (blank=True, null=True, help_text="Extra parameters for the model")
    created_at              =   models.DateTimeField    (auto_now_add=True, blank=True, null = True)
    updated_at              =   models.DateTimeField    (auto_now=True, blank=True, null=True)
    created_by              =   models.ForeignKey       (settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True, blank=True)
    updated_by              =   models.ForeignKey       (settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_updated_by", null=True, blank=True)
    has_object_permission   =   models.BooleanField     (default=False, help_text="Make it true if you want to add object level permissions for this record.")

    # Common Admin Meta for all models
    common_admin_meta = {
    }
    
    def check_object_permission(self, user, permission_codename):
        # Pass true if the user has the specified permission for this object.
        # It will allow all permissions if has_object_permission is False for this record.
        if not self.has_object_permission:
            return True

        """
        Check if the user has a specific permission for this object.
        """
        content_type    = ContentType.objects.get_for_model(self)
        permission      = Permission.objects.get(content_type=content_type, codename=permission_codename)

        return ObjectPermission.objects.filter(
            user            =   user,
            permission      =   permission,
            object_id       =   self.pk,
            content_type    =   content_type,
        ).exists()
    
    class Meta:
        abstract = True


# Image Master
class ImageMaster(CommonModel):
    name                =   models.CharField        (max_length=300)
    image               =   models.ImageField       (upload_to="image_master/")

    admin_meta = {
        'list_display': ['name', 'image','__str__', 'created_at', 'updated_at', 'created_by', 'updated_by', 'has_object_permission'],   
        'actions'   :   ['test_action',]
    }

    # Custom Action
    def test_action(self, obj, request):
        print(obj)

    def __str__(self):
        return mark_safe(
            '<div style="height:200px;width:200px;"><img src='+self.image.url+' style="object-fit:contain;height:100%;width:100%" alt=""></div>'
        )


# File Master
class FileMaster(CommonModel):
    name                =   models.CharField    (max_length=300)
    file                =   models.FileField    (upload_to='file_master/')

    admin_meta = {
        'list_display': ['name', 'file', '__str__', 'created_at', 'updated_at', 'created_by', 'updated_by'],   
    }

    def __str__(self):
        return str(self.name)





# MODELS GOES HERE
# Global Settings
class SiteSetting(CommonModel):
    logo                    =   models.ImageField   (blank=True,null=True,upload_to='settings/')
    favicon                 =   models.FileField    (blank=True,null=True,upload_to='settings/')
    global_head             =   models.TextField    (blank=True,null=True, help_text='Common <head> data. It will appear in all pages.')

    address                 =   models.TextField    (blank=True,null=True,max_length=500)
    contact_number          =   models.CharField    (blank=True,null=True,max_length=13)
    email                   =   models.EmailField   (blank=True,null=True)
    gst                     =   models.CharField    (blank=True,null=True,max_length=15, help_text="GST Number")
    extra_contact_details   =   HTMLField           (blank=True,null=True)

    facebook                =   models.URLField     (blank=True,null=True,max_length=100)
    instagram               =   models.URLField     (blank=True,null=True,max_length=100)
    twitter                 =   models.URLField     (blank=True,null=True,max_length=100)
    linkedin                =   models.URLField     (blank=True,null=True,max_length=100)

    vision                  =   models.TextField    (blank=True,null=True)
    mission                 =   models.TextField    (blank=True,null=True)
    values                  =   models.TextField    (blank=True,null=True)
    brochure                =   models.FileField    (blank=True,null=True,upload_to='settings/')
    
    navigation_menu         =   models.JSONField    (blank=True, null=True)

    about_us                =   HTMLField       (blank=True,null=True)
    terms_and_conditions    =   HTMLField       (blank=True,null=True)
    privacy_policy          =   HTMLField       (blank=True,null=True)
    return_policy           =   HTMLField       (blank=True,null=True)
    disclaimer              =   HTMLField       (blank=True,null=True)

    robots                  =   models.FileField    (blank=True,null=True,upload_to='settings/')
    

    # JSON FIELD SCHEMA
    key_value_pair_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "navMenu": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/menuItem"
            }
            }
        },
        "definitions": {
            "menuItem": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Unique identifier for the menu item."
                },
                "label": {
                    "type": "string",
                    "description": "Display text for the menu item."
                },
                "url": {
                    "type": "string",
                    "format": "uri",
                    "description": "URL link for the menu item."
                },
                "children": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/menuItem"
                },
                "description": "Nested menu items under this menu item."
                }
            },
            "required": ["id", "label"],
            "additionalProperties": False
            }
        }
    }

    # Dynamic admin
    admin_meta = {
        "json_fields": {
            "navigation_menu": {"schema":  json.dumps(key_value_pair_schema)},
        }
    }
    
    def __str__(self):
        return 'Edit Site Settings'

    class Meta:
        verbose_name_plural = "Site Setting"
    
    def save(self, *args, **kwargs):
        super(SiteSetting, self).save(*args, **kwargs)

class Startup(TenantBase):
    name            =   models.CharField(max_length=100)
    paid_until      =   models.DateField()
    on_trial        =   models.BooleanField()
    created_on      =   models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class Domain(DomainMixin):
    pass

class TenantUser(UserProfile):
    name    =   models.CharField(max_length=100)




