# DO NOT EDIT! This file is automatically generated

import marshmallow

from commercetools import types

__all__ = [
    "ApiClientDraftSchema",
    "ApiClientPagedQueryResponseSchema",
    "ApiClientSchema",
]


class ApiClientDraftSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.ApiClientDraft`."
    name = marshmallow.fields.String(allow_none=True)
    scope = marshmallow.fields.String(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.ApiClientDraft(**data)


class ApiClientPagedQueryResponseSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.ApiClientPagedQueryResponse`."
    count = marshmallow.fields.Integer(allow_none=True)
    total = marshmallow.fields.Integer(allow_none=True, missing=None)
    offset = marshmallow.fields.Integer(allow_none=True)
    results = marshmallow.fields.Nested(
        nested="commercetools.schemas._api_client.ApiClientSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.ApiClientPagedQueryResponse(**data)


class ApiClientSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.ApiClient`."
    id = marshmallow.fields.String(allow_none=True)
    name = marshmallow.fields.String(allow_none=True)
    scope = marshmallow.fields.String(allow_none=True)
    created_at = marshmallow.fields.DateTime(allow_none=True, data_key="createdAt")
    last_used_at = marshmallow.fields.Date(
        allow_none=True, missing=None, data_key="lastUsedAt"
    )
    secret = marshmallow.fields.String(allow_none=True, missing=None)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.ApiClient(**data)
