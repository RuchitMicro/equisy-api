from django.contrib import admin

# Imports for Dynamic app registrations
from django.apps            import apps

# Models
from web.models             import *

# Json Widget
from .widget                import JsonEditorWidget


admin.site.site_header = "Equisy Developer's Admin"


exempt                  =   []
class GenericAdmin(admin.ModelAdmin):
    
    # Common actions for all models
    @admin.action
    def bypass_permissions(self, request, queryset):
        for obj in queryset:
            obj.has_object_permission = False
            obj.save()
            
    # Common actions for all models
    actions = ['bypass_permissions']

    def __init__(self, model, admin_site):
        '''
        Dynamic admin meta from common model
        adding common admin meta into the model admin meta
        We have done this so that the common admin meta does not get overwritten in the child class
        '''
        self.model          =   model
        common_admin_meta   =   model.common_admin_meta if hasattr(model, 'common_admin_meta') else {}
        model.admin_meta    =   {**common_admin_meta, **model.admin_meta} if hasattr(model, 'admin_meta') else common_admin_meta

        # Dynamic admin meta from model
        # Specify a static dictionary in model
        try:
            # Admin Meta
            if model.admin_meta:
                for k,v in model.admin_meta.items():
                    if k != 'actions': # Actions are handled separately
                        self.__setattr__(k,v)
        except:
            pass
        
        # Dynamic Actions from model
        # Specify a key 'actions' in the admin_meta dictionary in model
        try:
            if 'actions' in model.admin_meta:
                for action_name in model.admin_meta['actions']:
                    # Ensure action_name is a string
                    if isinstance(action_name, str):
                        action_function = getattr(self.model, action_name, None)
                        if callable(action_function):
                            self.add_action(action_function, action_name)
        except Exception as e:
            print(e)
            # Handle or log the exception
            pass
        super().__init__(model, admin_site)

        
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        # Check if the field is a JSONField
        if isinstance(db_field, models.JSONField):
            # Retrieve the schema configuration for JSON fields
            json_fields_meta = self.model.admin_meta.get('json_fields', {})

            # Retrieve the schema for the specific field, if defined
            json_schema = json_fields_meta.get(db_field.name, {}).get('schema')

            if json_schema:
                # Initialize the custom widget with the specified schema
                kwargs['widget'] = JsonEditorWidget(schema=json_schema)
            else:
                # Else load the django-jsoneditor widget 
                kwargs['widget'] = JSONEditor()

        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        # Define the fieldsets
        common_fields   =   [field.name for field in CommonModel._meta.fields if field.editable]
        other_fields    =   [field.name for field in self.model._meta.fields if (field.name not in common_fields and field.editable and field.name != 'id')]

        fieldsets = [
            (self.model._meta.object_name, {
                'fields': other_fields,
            }),
            ('Meta Data', {
                'fields': common_fields,
            }),
        ]

        return fieldsets
    
    def get_readonly_fields(self, request, obj=None):
        # Get a list of non-editable fields
        readonly_fields = [field.name for field in self.model._meta.fields if (not field.editable or field.name == 'id')]

        return readonly_fields
    
    # Function to add actions to the admin class
    def add_action(self, action_function, action_name):
        def wrapper_action(modeladmin, request, queryset):
            for obj in queryset:
                action_method = getattr(obj, action_name)
                if callable(action_method):
                    action_method(obj, request)

        unique_action_name                  = f'admin_action_{self.model.__name__}_{action_name}'
        wrapper_action.__name__             = unique_action_name
        wrapper_action.short_description    = action_name.replace('_', ' ').title()

        if unique_action_name not in [action for action in self.actions]:
            self.actions.append(wrapper_action)
            print(f'Added action {unique_action_name} to {self.model.__name__}')
            
    # Custom Media so that we can add custom js files
    class Media:
        js = ('https://code.jquery.com/jquery-3.7.0.js', )





app = apps.get_app_config('web')
for model_name, model in app.models.items():
    if model_name not in exempt:
        admin.site.register(model, GenericAdmin)