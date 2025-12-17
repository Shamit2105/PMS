# serializers.py
from rest_framework import serializers
import uuid
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from . import errors
from .errors import PMValidationError, PMDataIntegrityException



class BaseSerializer(serializers.Serializer):
    """
    Base serializer with dynamic field filtering capabilities.
    Supports field whitelisting(allowed), blacklisting(blocked), and audit field removal.
    """
    
    AUDIT_FIELDS = ['created_at', 'updated_at', 'created_by', 'updated_by', ]
    
    def __init__(self, *args, **kwargs):
        
        allowed_fields = kwargs.pop('allowed_fields', [])
        removed_fields = kwargs.pop('removed_fields', [])
        remove_audit_fields = kwargs.pop('remove_audit', False)
        
        # to convert field lists to nested maps for efficient lookup
        self._allowed_fields_map = self.extract_nested_fields(allowed_fields)
        self._removed_fields_map = self.extract_nested_fields(removed_fields)
        self._remove_audit = remove_audit_fields
        
        super().__init__(*args, **kwargs)
        
        # apply field filtering
        self._apply_allowed_fields()
        self._apply_removed_fields()
        
        # remove audit fields if requested
        if remove_audit_fields:
            self._remove_audit_fields()
    
    @staticmethod
    def extract_nested_fields(fields_list):
        """
        Convert a list of field paths into a nested dictionary structure.
        
        Args:
            fields_list (list): List of field names with dot notation for nesting
        
        Returns:
            dict: Nested dictionary representing field hierarchy
            
        Example:
            ['id', 'user.profile.name'] -> {
                'id': {},
                'user': {
                    'profile': {
                        'name': {}
                    }
                }
            }
        """
        if not fields_list:
            return {}
        
        result = {}
        
        for field_path in fields_list:
            if not field_path or not isinstance(field_path, str):
                continue
                
            parts = field_path.split('.')
            current = result
            
            for part in parts:
                part = part.strip() #removes initial and final spaces
                if not part:
                    continue
                    
                if part not in current:
                    current[part] = {}
                current = current[part]
        
        return result
    
    def _apply_allowed_fields(self):
        """
        Apply field whitelist filtering.
        Only keeps fields specified in allowed_fields.
        """
        if not self._allowed_fields_map:
            return
        
        # get all top-level field names from the allowed map
        allowed_keys = set(self._allowed_fields_map.keys())
        
        # remove fields not in the allowed list
        for field_name in list(self.fields.keys()):
            if field_name not in allowed_keys:
                self.fields.pop(field_name, None)
        
        # apply filtering to nested serializers
        for field_name, nested_map in self._allowed_fields_map.items():
            if nested_map and field_name in self.fields:
                field = self.fields[field_name]
                self._apply_nested_filtering(field, nested_map)
    
    def _apply_nested_filtering(self, field, nested_map):
        """
        Apply filtering to nested serializer fields.
        
        Args:
            field: Serializer field (could be nested serializer or list serializer)
            nested_map (dict): Map of nested fields to include
        """
        # Handle ListSerializer (many=True)
        if isinstance(field, serializers.ListSerializer):
            child = field.child
            if isinstance(child, serializers.BaseSerializer):
                # Create a new serializer class with filtered fields
                self._create_filtered_serializer(child, nested_map, field)
        
        # Handle regular nested serializer
        elif isinstance(field, serializers.BaseSerializer):
            self._create_filtered_serializer(field, nested_map)
    
    def _create_filtered_serializer(self, serializer, nested_map, parent_field=None):
        """
        Create a filtered version of a nested serializer.
        
        Args:
            serializer: The nested serializer to filter
            nested_map (dict): Fields to include in the nested serializer
            parent_field: Parent field (for ListSerializer)
        """
        # Create a new serializer class that filters its fields
        class FilteredSerializer(serializer.__class__):
            def __init__(self, *args, **kwargs):
                # Don't pass filtering kwargs to avoid infinite recursion
                kwargs.pop('allowed_fields', None)
                kwargs.pop('removed_fields', None)
                kwargs.pop('remove_audit', None)
                super().__init__(*args, **kwargs)
                
                # Apply field filtering to this nested serializer
                self._filter_nested_fields(nested_map)
            
            def _filter_nested_fields(self, filter_map):
                """Filter fields in this nested serializer."""
                if not filter_map:
                    return
                
                # Get allowed top-level fields
                allowed_keys = set(filter_map.keys())
                
                # Remove fields not in allowed list
                for field_name in list(self.fields.keys()):
                    if field_name not in allowed_keys:
                        self.fields.pop(field_name, None)
                
                # Recursively apply to deeper nesting
                for field_name, inner_map in filter_map.items():
                    if inner_map and field_name in self.fields:
                        nested_field = self.fields[field_name]
                        if isinstance(nested_field, serializers.BaseSerializer):
                            # Recursively filter
                            nested_field._filter_nested_fields(inner_map)
                        elif (isinstance(nested_field, serializers.ListSerializer) and 
                              isinstance(nested_field.child, serializers.BaseSerializer)):
                            nested_field.child._filter_nested_fields(inner_map)
        
        # Replace the original serializer with the filtered version
        if parent_field:
            # For ListSerializer, replace the child
            parent_field.child = FilteredSerializer(
                instance=serializer.instance,
                data=serializer.initial_data,
                context=serializer.context
            )
        else:
            # For regular serializer, replace it
            self.fields[serializer.field_name] = FilteredSerializer(
                instance=serializer.instance,
                data=serializer.initial_data,
                context=serializer.context
            )
    
    def _apply_removed_fields(self):
        """
        Apply field blacklist filtering.
        Removes fields specified in removed_fields.
        """
        if not self._removed_fields_map:
            return
        
        # Remove top-level fields
        for field_name in self._removed_fields_map.keys():
            if field_name in self.fields:
                self.fields.pop(field_name, None)
        
        # Apply to nested serializers
        for field_name, nested_map in self._removed_fields_map.items():
            if field_name in self.fields:
                field = self.fields[field_name]
                self._remove_nested_fields(field, nested_map)
    
    def _remove_nested_fields(self, field, nested_map):
        """
        Remove fields from nested serializers.
        
        Args:
            field: Serializer field
            nested_map (dict): Map of nested fields to remove
        """
        # Handle ListSerializer
        if isinstance(field, serializers.ListSerializer):
            child = field.child
            if isinstance(child, serializers.BaseSerializer):
                self._remove_from_nested_serializer(child, nested_map)
        
        # Handle regular nested serializer
        elif isinstance(field, serializers.BaseSerializer):
            self._remove_from_nested_serializer(field, nested_map)
    
    def _remove_from_nested_serializer(self, serializer, nested_map):
        """
        Remove fields from a nested serializer.
        
        Args:
            serializer: Nested serializer
            nested_map (dict): Fields to remove
        """
        # Remove top-level fields in nested serializer
        for field_name in nested_map.keys():
            if field_name in serializer.fields:
                serializer.fields.pop(field_name, None)
        
        # Recursively remove from deeper nesting
        for field_name, inner_map in nested_map.items():
            if inner_map and field_name in serializer.fields:
                nested_field = serializer.fields[field_name]
                if isinstance(nested_field, serializers.BaseSerializer):
                    self._remove_from_nested_serializer(nested_field, inner_map)
                elif (isinstance(nested_field, serializers.ListSerializer) and 
                      isinstance(nested_field.child, serializers.BaseSerializer)):
                    self._remove_from_nested_serializer(nested_field.child, inner_map)
    
    def _remove_audit_fields(self):
        """
        Remove common audit fields from the serializer.
        """
        for audit_field in self.AUDIT_FIELDS:
            if audit_field in self.fields:
                self.fields.pop(audit_field, None)
        
        # Also remove from nested serializers
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.BaseSerializer):
                field._remove_audit_fields()
            elif (isinstance(field, serializers.ListSerializer) and 
                  isinstance(field.child, serializers.BaseSerializer)):
                field.child._remove_audit_fields()
    
    def get_field_names(self):
        """
        Get the names of all fields in the serializer.
        Useful for debugging or introspection.
        """
        return list(self.fields.keys())
    
    def to_representation(self, instance):
        """
        Override to ensure filtered fields work correctly.
        """
        representation = super().to_representation(instance)
        
        # Convert UUID fields to string for JSON serialization
        for key, value in representation.items():
            if isinstance(value, uuid.UUID):
                representation[key] = str(value)
        
        return representation

class BaseModelSerializer(serializers.ModelSerializer, BaseSerializer):
    """
    Model serializer with dynamic field filtering, audit fields, and unique_together validation.
    
    Features:
    1. Dynamic field filtering (inherited from BaseSerializer)
    2. Built-in audit fields
    3. Unique together validation
    4. Soft delete support
    5. Error handling with custom error codes
    """
    
    # Common audit/status fields
    id = serializers.UUIDField(
        read_only=True, 
        default=uuid.uuid4,
        help_text="Unique record identifier"
    )
    is_active = serializers.BooleanField(
        read_only=True,
        default=True,
        help_text="Indicates if the record is active"
    )
    is_deleted = serializers.BooleanField(
        read_only=True,
        default=False,
        help_text="Indicates if the record is soft deleted"
    )
    is_deletable = serializers.BooleanField(
        read_only=True,
        default=True,
        help_text="Indicates if the record can be deleted"
    )
    
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(read_only=True)
    updated_by = serializers.CharField(read_only=True)
    
    
    AUDIT_FIELDS = BaseSerializer.AUDIT_FIELDS + [
        'created_at', 'updated_at', 'created_by', 'updated_by', 
    ]
    
    class Meta:
        abstract = True
        fields = [
            'id', 'is_active', 
            'created_at', 'updated_at', 'created_by', 'updated_by',
        ]
        read_only_fields = [
            'id', 'is_active',  
            'created_at', 'updated_at', 'created_by', 'updated_by', 
        ]
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the serializer with field filtering.
        Handles the MRO (Method Resolution Order) correctly.
        """
        # First, call ModelSerializer.__init__ to set up fields
        # We need to handle the field filtering in a specific order
        
        # Extract filtering parameters before passing to parent
        self._filter_kwargs = {
            'allowed_fields': kwargs.pop('allowed_fields', []),
            'removed_fields': kwargs.pop('removed_fields', []),
            'remove_audit': kwargs.pop('remove_audit', False)
        }
        
        super().__init__(*args, **kwargs)
        
        # Now apply BaseSerializer's field filtering
        self._initialize_field_filtering()
    
    def _initialize_field_filtering(self):
        """
        Apply field filtering after ModelSerializer initialization.
        This ensures fields are created before we try to filter them.
        """
        # Convert field lists to nested maps
        self._allowed_fields_map = self.extract_nested_fields(
            self._filter_kwargs['allowed_fields']
        )
        self._removed_fields_map = self.extract_nested_fields(
            self._filter_kwargs['removed_fields']
        )
        self._remove_audit = self._filter_kwargs['remove_audit']
        
        # Apply field filtering
        self._apply_allowed_fields()
        self._apply_removed_fields()
        
        # Remove audit fields if requested
        if self._remove_audit:
            self._remove_audit_fields()
    
    def is_valid(self, *, raise_exception=False):
        """
        Run default validation + unique_together validation with custom errors.
        
        Args:
            raise_exception (bool): If True, raises exception on validation error
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Run standard validation
        super().is_valid(raise_exception=False)
        
        is_violated = False
        
        # Run unique_together validation if no other errors
        if not self._errors:
            is_violated = self.unique_together_validation()
        
        # If there are errors, raise exception if requested
        if self._errors:
            if raise_exception:
                serializers.ValidationError(is_violated)
        
        return not bool(self._errors)
    
    def __get_unique_fields(self):
        """
        Extract unique_together field sets from model Meta.
        
        Returns:
            list: List of dictionaries with field-value pairs for unique validation
        """
        meta = getattr(self.Meta.model, "_meta")
        unique_fields = getattr(meta, "unique_together", [])
        
        fields = []
        
        for unique_set in unique_fields:
            field_set = {}
            
            for item in unique_set:
                # Check if field is in validated_data
                if item in self.validated_data:
                    item_value = self.validated_data[item]
                    
                    # Use case-insensitive lookup for string fields
                    if isinstance(item_value, str):
                        lookup_field = f"{item}__iexact"
                    else:
                        lookup_field = item
                    
                    field_set[lookup_field] = item_value
            
            # Validate that we have all required fields
            if field_set:
                expected_len = len(field_set)
                actual_len = len(unique_set)
                
                if expected_len != actual_len:
                    
                    raise PMDataIntegrityException(
                        f"Unique Validation Failed. Unique Fields: {unique_set}, "
                        f"Serializer Fields: {list(field_set.keys())}. "
                        f"Expected {actual_len} fields, got {expected_len}."
                    )
            
            if field_set:
                fields.append(field_set)
        
        return fields
    
    def unique_together_validation(self):
        """
        Check for unique_together violations and add errors if needed.
        
        Returns:
            bool: True if unique constraint was violated, False otherwise
        """
        is_violated = False
        unique_field_sets = self.__get_unique_fields()
        
        if not unique_field_sets:
            return is_violated
        
        for field_set in unique_field_sets:
            try:
                # Try to get existing object with the same unique field values
                # Note: using all_objects to include soft-deleted records if needed
                obj = self.Meta.model.all_objects.get(**field_set)
                
                # Skip if we're updating the same object
                if not (self.instance and obj.id == self.instance.id):
                    error_fields = [f.split('__')[0] for f in field_set.keys()]
                    
                    # Format error message
                    if len(error_fields) == 1:
                        message = "This value already exists."
                    else:
                        message = "Combination of these values already exists."
                    
                    # Create error key (comma-separated field names)
                    err_key = ", ".join(error_fields)
                    
                    # Add error to serializer
                    if err_key not in self._errors:
                        self._errors[err_key] = [message]
                    
                    is_violated = True
                    
            except ObjectDoesNotExist:
                # No existing record with these values - good!
                pass
            except Exception as e:
                # Log unexpected errors but don't fail validation
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error in unique_together_validation: {str(e)}")
        
        return is_violated
    
    
    def create(self, validated_data):
        request = self.context.get('request')

        if request and hasattr(request, 'user'):
            validated_data.setdefault('created_by', request.user)
            validated_data.setdefault('updated_by', request.user)

        validated_data.setdefault('is_active', True)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Override update to handle audit fields and custom logic.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['updated_by'] = request.user
        # Remove audit fields that shouldn't be updated
        for audit_field in self.AUDIT_FIELDS:
            validated_data.pop(audit_field, None)
        
        # Call parent update method
        return super().update(instance, validated_data)
    
    def get_field_info(self, field_name):
        """
        Get information about a specific field.
        Useful for generating documentation or forms.
        
        Args:
            field_name (str): Name of the field
            
        Returns:
            dict: Field information including type, help text, etc.
        """
        field = self.fields.get(field_name)
        
        if not field:
            return None
        
        info = {
            'type': field.__class__.__name__,
            'required': field.required,
            'read_only': field.read_only,
            'help_text': getattr(field, 'help_text', ''),
            'label': getattr(field, 'label', field_name),
        }
        
        # Add additional info for specific field types
        if hasattr(field, 'max_length'):
            info['max_length'] = field.max_length
        if hasattr(field, 'min_length'):
            info['min_length'] = field.min_length
        
        return info


