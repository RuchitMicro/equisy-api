
# Enhanced Django Admin Customization Script Documentation

## Overview

This updated documentation details an enhanced Django script for customizing the admin interface. It dynamically registers models with custom admin classes, featuring improved handling for JSON fields, dynamic actions, and fieldsets organization.

## Table of Contents

- [Overview](#overview)
- [Components](#components)
  - [Imports](#imports)
  - [Global Configuration](#global-configuration)
  - [Exempt Models](#exempt-models)
  - [GenericAdmin Class](#genericadmin-class)
  - [Dynamic Model Registration](#dynamic-model-registration)
- [Key Concepts](#key-concepts)
- [Usage](#usage)
- [Conclusion](#conclusion)

## Components

### Imports

- `from django.contrib import admin`
- `from django.apps import apps`
- `from tabbed_admin import TabbedModelAdmin` (Unused in the script)
- `from web.models import *`
- `from .widget import JsonEditorWidget`

### Global Configuration

```python
admin.site.site_header = "Equisy Developer's Admin"
```

Sets a custom header for the admin site.

### Exempt Models

```python
exempt = []
```

List of model names to exclude from dynamic registration.

### GenericAdmin Class

#### Purpose

Extends `admin.ModelAdmin` for flexible admin interfaces, customizing fieldsets, read-only fields, form fields, and dynamic actions.

#### Methods

1. **`__init__`:**
   - Dynamically assigns attributes from `admin_meta` in models.
   - Adds custom actions from `admin_meta['actions']`.
   - Inherits from the superclass constructor.

2. **`formfield_for_dbfield`:**
   - Special handling for `models.JSONField` using `JsonEditorWidget` or `JSONEditor`.

3. **`get_fieldsets`:**
   - Organizes fields into common and model-specific fieldsets.

4. **`get_readonly_fields`:**
   - Identifies read-only fields based on editability and name.

5. **`add_action`:**
   - Adds custom actions to the admin class dynamically.

6. **`Media`:**
   - Defines custom JavaScript files to include in the admin.

### Dynamic Model Registration

Automatically registers models in the `web` app with the admin using `GenericAdmin`, except those listed in `exempt`.

## Key Concepts

- **Dynamic Administration**: Adaptable and scalable approach.
- **Enhanced JSON Field Management**: Advanced handling with custom widgets.
- **Custom Actions**: Ability to add model-specific actions dynamically.
- **Fieldsets Organization**: Clear separation of common and unique fields.

## Usage

Designed for use in the `models.py` of a Django app, it registers models with enhanced admin functionalities.

```python
admin_meta = {
   # List display options
   'list_display': ['field1', 'field2', 'custom_method'],
   'list_display_links': ['field1'],
   'list_editable': ['field2'],
   'list_filter': ['field3', 'field4'],
   'list_per_page': 25,
   'list_select_related': False,
   'list_max_show_all': 100,
   'list_view': 'custom_list_view',

   # Search and ordering
   'search_fields': ['field1', 'field5__related_field'],
   'ordering': ['-field1'],

   # Form and field options
   'fields': ['field1', 'field2', ('field3', 'field4')],
   'exclude': ['field5'],
   'fieldsets': [
      ('Section 1', {'fields': ['field1', 'field2']}),
      ('Section 2', {'fields': ['field3'], 'classes': ['collapse']}),
   ],
   'form': CustomForm,
   'filter_horizontal': ['field6'],
   'filter_vertical': ['field7'],
   'radio_fields': {'field8': admin.HORIZONTAL},
   'prepopulated_fields': {"slug": ("title",)},
   'readonly_fields': ['field9'],
   'autocomplete_fields': ['field10'],

   # Date hierarchy
   'date_hierarchy': 'publish_date',

   # Custom actions
   'actions': ['custom_action'],

   # Media class for custom JavaScript and CSS
   'Media': {
      'js': ('custom.js',),
      'css': {
         'all': ('custom.css',)
      }
   },

   # Inlines
   'inlines': [RelatedModelInline],

   # JSON field configuration
   'json_fields': {
      'json_field_name': {
         'schema': json_schema
      }
   },

   # Misc
   'save_as': True,
   'save_on_top': True,
   'save_as_continue': True,
   'preserve_filters': True,
   'change_list_template': 'custom_change_list.html',
   'add_form_template': 'custom_add_form.html',
   'change_form_template': 'custom_change_form.html',
   'delete_confirmation_template': 'custom_delete_confirmation.html',
   'delete_selected_confirmation_template': 'custom_delete_selected_confirmation.html',
   'object_history_template': 'custom_object_history.html',

   # Permissions
   'has_add_permission': custom_has_add_permission_function,
   'has_change_permission': custom_has_change_permission_function,
   'has_delete_permission': custom_has_delete_permission_function,
   'has_view_permission': custom_has_view_permission_function,

   # Custom admin methods or attributes
   'custom_attribute': 'value',
   'custom_method': custom_admin_method,
}
```

## Conclusion

The script offers a more sophisticated admin interface, with dynamic model registration, specialized JSON field handling, dynamic actions, and organized fieldsets, thereby enhancing the efficiency and usability of the Django admin.