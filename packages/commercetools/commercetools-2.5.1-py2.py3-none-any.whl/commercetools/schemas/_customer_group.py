# DO NOT EDIT! This file is automatically generated

import marshmallow

from commercetools import helpers, types
from commercetools.schemas._base import (
    PagedQueryResponseSchema,
    UpdateActionSchema,
    UpdateSchema,
)
from commercetools.schemas._common import ReferenceSchema, ResourceSchema
from commercetools.schemas._type import FieldContainerField

__all__ = [
    "CustomerGroupChangeNameActionSchema",
    "CustomerGroupDraftSchema",
    "CustomerGroupPagedQueryResponseSchema",
    "CustomerGroupReferenceSchema",
    "CustomerGroupSchema",
    "CustomerGroupSetCustomFieldActionSchema",
    "CustomerGroupSetCustomTypeActionSchema",
    "CustomerGroupSetKeyActionSchema",
    "CustomerGroupUpdateActionSchema",
    "CustomerGroupUpdateSchema",
]


class CustomerGroupDraftSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.CustomerGroupDraft`."
    key = marshmallow.fields.String(allow_none=True, missing=None)
    group_name = marshmallow.fields.String(allow_none=True, data_key="groupName")
    custom = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.CustomFieldsSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.CustomerGroupDraft(**data)


class CustomerGroupPagedQueryResponseSchema(PagedQueryResponseSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomerGroupPagedQueryResponse`."
    results = marshmallow.fields.Nested(
        nested="commercetools.schemas._customer_group.CustomerGroupSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.CustomerGroupPagedQueryResponse(**data)


class CustomerGroupReferenceSchema(ReferenceSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomerGroupReference`."
    obj = marshmallow.fields.Nested(
        nested="commercetools.schemas._customer_group.CustomerGroupSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type_id"]
        return types.CustomerGroupReference(**data)


class CustomerGroupSchema(ResourceSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomerGroup`."
    key = marshmallow.fields.String(allow_none=True, missing=None)
    name = marshmallow.fields.String(allow_none=True)
    custom = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.CustomFieldsSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.CustomerGroup(**data)


class CustomerGroupUpdateActionSchema(UpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomerGroupUpdateAction`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.CustomerGroupUpdateAction(**data)


class CustomerGroupUpdateSchema(UpdateSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomerGroupUpdate`."
    actions = marshmallow.fields.List(
        helpers.Discriminator(
            discriminator_field=("action", "action"),
            discriminator_schemas={
                "changeName": "commercetools.schemas._customer_group.CustomerGroupChangeNameActionSchema",
                "setCustomField": "commercetools.schemas._customer_group.CustomerGroupSetCustomFieldActionSchema",
                "setCustomType": "commercetools.schemas._customer_group.CustomerGroupSetCustomTypeActionSchema",
                "setKey": "commercetools.schemas._customer_group.CustomerGroupSetKeyActionSchema",
            },
            unknown=marshmallow.EXCLUDE,
            allow_none=True,
        ),
        allow_none=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.CustomerGroupUpdate(**data)


class CustomerGroupChangeNameActionSchema(CustomerGroupUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomerGroupChangeNameAction`."
    name = marshmallow.fields.String(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.CustomerGroupChangeNameAction(**data)


class CustomerGroupSetCustomFieldActionSchema(CustomerGroupUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomerGroupSetCustomFieldAction`."
    name = marshmallow.fields.String(allow_none=True)
    value = marshmallow.fields.Raw(allow_none=True, missing=None)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.CustomerGroupSetCustomFieldAction(**data)


class CustomerGroupSetCustomTypeActionSchema(CustomerGroupUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomerGroupSetCustomTypeAction`."
    type = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.TypeReferenceSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
    )
    fields = FieldContainerField(allow_none=True, missing=None)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.CustomerGroupSetCustomTypeAction(**data)


class CustomerGroupSetKeyActionSchema(CustomerGroupUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomerGroupSetKeyAction`."
    key = marshmallow.fields.String(allow_none=True, missing=None)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.CustomerGroupSetKeyAction(**data)
