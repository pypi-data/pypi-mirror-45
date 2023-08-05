# DO NOT EDIT! This file is automatically generated

import marshmallow
import marshmallow_enum

from commercetools import helpers, types
from commercetools.schemas._base import (
    PagedQueryResponseSchema,
    UpdateActionSchema,
    UpdateSchema,
)
from commercetools.schemas._common import ResourceSchema

__all__ = [
    "AzureEventGridDestinationSchema",
    "AzureServiceBusDestinationSchema",
    "ChangeSubscriptionSchema",
    "DeliveryCloudEventsFormatSchema",
    "DeliveryFormatSchema",
    "DeliveryPlatformFormatSchema",
    "DestinationSchema",
    "GoogleCloudPubSubDestinationSchema",
    "IronMqDestinationSchema",
    "MessageDeliverySchema",
    "MessageSubscriptionSchema",
    "PayloadNotIncludedSchema",
    "ResourceCreatedDeliverySchema",
    "ResourceDeletedDeliverySchema",
    "ResourceUpdatedDeliverySchema",
    "SnsDestinationSchema",
    "SqsDestinationSchema",
    "SubscriptionChangeDestinationActionSchema",
    "SubscriptionDeliverySchema",
    "SubscriptionDraftSchema",
    "SubscriptionPagedQueryResponseSchema",
    "SubscriptionSchema",
    "SubscriptionSetChangesActionSchema",
    "SubscriptionSetKeyActionSchema",
    "SubscriptionSetMessagesActionSchema",
    "SubscriptionUpdateActionSchema",
    "SubscriptionUpdateSchema",
]


class ChangeSubscriptionSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.ChangeSubscription`."
    resource_type_id = marshmallow.fields.String(
        allow_none=True, data_key="resourceTypeId"
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.ChangeSubscription(**data)


class DeliveryFormatSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.DeliveryFormat`."
    type = marshmallow.fields.String(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type"]
        return types.DeliveryFormat(**data)


class DestinationSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.Destination`."
    type = marshmallow.fields.String(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type"]
        return types.Destination(**data)


class MessageSubscriptionSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.MessageSubscription`."
    resource_type_id = marshmallow.fields.String(
        allow_none=True, data_key="resourceTypeId"
    )
    types = marshmallow.fields.List(
        marshmallow.fields.String(allow_none=True), missing=None
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.MessageSubscription(**data)


class PayloadNotIncludedSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.PayloadNotIncluded`."
    reason = marshmallow.fields.String(allow_none=True)
    payload_type = marshmallow.fields.String(allow_none=True, data_key="payloadType")

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.PayloadNotIncluded(**data)


class SubscriptionDeliverySchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.SubscriptionDelivery`."
    project_key = marshmallow.fields.String(allow_none=True, data_key="projectKey")
    notification_type = marshmallow.fields.String(
        allow_none=True, data_key="notificationType"
    )
    resource = helpers.Discriminator(
        discriminator_field=("typeId", "type_id"),
        discriminator_schemas={
            "cart-discount": "commercetools.schemas._cart_discount.CartDiscountReferenceSchema",
            "cart": "commercetools.schemas._cart.CartReferenceSchema",
            "category": "commercetools.schemas._category.CategoryReferenceSchema",
            "channel": "commercetools.schemas._channel.ChannelReferenceSchema",
            "key-value-document": "commercetools.schemas._custom_object.CustomObjectReferenceSchema",
            "customer-group": "commercetools.schemas._customer_group.CustomerGroupReferenceSchema",
            "customer": "commercetools.schemas._customer.CustomerReferenceSchema",
            "discount-code": "commercetools.schemas._discount_code.DiscountCodeReferenceSchema",
            "inventory-entry": "commercetools.schemas._inventory.InventoryEntryReferenceSchema",
            "order-edit": "commercetools.schemas._order_edit.OrderEditReferenceSchema",
            "order": "commercetools.schemas._order.OrderReferenceSchema",
            "payment": "commercetools.schemas._payment.PaymentReferenceSchema",
            "product-discount": "commercetools.schemas._product_discount.ProductDiscountReferenceSchema",
            "product-type": "commercetools.schemas._product_type.ProductTypeReferenceSchema",
            "product": "commercetools.schemas._product.ProductReferenceSchema",
            "review": "commercetools.schemas._review.ReviewReferenceSchema",
            "shipping-method": "commercetools.schemas._shipping_method.ShippingMethodReferenceSchema",
            "shopping-list": "commercetools.schemas._shopping_list.ShoppingListReferenceSchema",
            "state": "commercetools.schemas._state.StateReferenceSchema",
            "tax-category": "commercetools.schemas._tax_category.TaxCategoryReferenceSchema",
            "type": "commercetools.schemas._type.TypeReferenceSchema",
            "zone": "commercetools.schemas._zone.ZoneReferenceSchema",
        },
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
    )
    resource_user_provided_identifiers = marshmallow.fields.Nested(
        nested="commercetools.schemas._message.UserProvidedIdentifiersSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
        data_key="resourceUserProvidedIdentifiers",
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["notification_type"]
        return types.SubscriptionDelivery(**data)


class SubscriptionDraftSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.SubscriptionDraft`."
    changes = marshmallow.fields.Nested(
        nested="commercetools.schemas._subscription.ChangeSubscriptionSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
        missing=None,
    )
    destination = helpers.Discriminator(
        discriminator_field=("type", "type"),
        discriminator_schemas={
            "EventGrid": "commercetools.schemas._subscription.AzureEventGridDestinationSchema",
            "AzureServiceBus": "commercetools.schemas._subscription.AzureServiceBusDestinationSchema",
            "GoogleCloudPubSub": "commercetools.schemas._subscription.GoogleCloudPubSubDestinationSchema",
            "IronMQ": "commercetools.schemas._subscription.IronMqDestinationSchema",
            "SNS": "commercetools.schemas._subscription.SnsDestinationSchema",
            "SQS": "commercetools.schemas._subscription.SqsDestinationSchema",
        },
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
    )
    key = marshmallow.fields.String(allow_none=True, missing=None)
    messages = marshmallow.fields.Nested(
        nested="commercetools.schemas._subscription.MessageSubscriptionSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
        missing=None,
    )
    format = helpers.Discriminator(
        discriminator_field=("type", "type"),
        discriminator_schemas={
            "CloudEvents": "commercetools.schemas._subscription.DeliveryCloudEventsFormatSchema",
            "Platform": "commercetools.schemas._subscription.DeliveryPlatformFormatSchema",
        },
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.SubscriptionDraft(**data)


class SubscriptionPagedQueryResponseSchema(PagedQueryResponseSchema):
    "Marshmallow schema for :class:`commercetools.types.SubscriptionPagedQueryResponse`."
    results = marshmallow.fields.Nested(
        nested="commercetools.schemas._subscription.SubscriptionSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.SubscriptionPagedQueryResponse(**data)


class SubscriptionSchema(ResourceSchema):
    "Marshmallow schema for :class:`commercetools.types.Subscription`."
    changes = marshmallow.fields.Nested(
        nested="commercetools.schemas._subscription.ChangeSubscriptionSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
    )
    destination = helpers.Discriminator(
        discriminator_field=("type", "type"),
        discriminator_schemas={
            "EventGrid": "commercetools.schemas._subscription.AzureEventGridDestinationSchema",
            "AzureServiceBus": "commercetools.schemas._subscription.AzureServiceBusDestinationSchema",
            "GoogleCloudPubSub": "commercetools.schemas._subscription.GoogleCloudPubSubDestinationSchema",
            "IronMQ": "commercetools.schemas._subscription.IronMqDestinationSchema",
            "SNS": "commercetools.schemas._subscription.SnsDestinationSchema",
            "SQS": "commercetools.schemas._subscription.SqsDestinationSchema",
        },
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
    )
    key = marshmallow.fields.String(allow_none=True, missing=None)
    messages = marshmallow.fields.Nested(
        nested="commercetools.schemas._subscription.MessageSubscriptionSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
    )
    format = helpers.Discriminator(
        discriminator_field=("type", "type"),
        discriminator_schemas={
            "CloudEvents": "commercetools.schemas._subscription.DeliveryCloudEventsFormatSchema",
            "Platform": "commercetools.schemas._subscription.DeliveryPlatformFormatSchema",
        },
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
    )
    status = marshmallow_enum.EnumField(types.SubscriptionHealthStatus, by_value=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.Subscription(**data)


class SubscriptionUpdateActionSchema(UpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.SubscriptionUpdateAction`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.SubscriptionUpdateAction(**data)


class SubscriptionUpdateSchema(UpdateSchema):
    "Marshmallow schema for :class:`commercetools.types.SubscriptionUpdate`."
    actions = marshmallow.fields.List(
        helpers.Discriminator(
            discriminator_field=("action", "action"),
            discriminator_schemas={
                "changeDestination": "commercetools.schemas._subscription.SubscriptionChangeDestinationActionSchema",
                "setChanges": "commercetools.schemas._subscription.SubscriptionSetChangesActionSchema",
                "setKey": "commercetools.schemas._subscription.SubscriptionSetKeyActionSchema",
                "setMessages": "commercetools.schemas._subscription.SubscriptionSetMessagesActionSchema",
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
        return types.SubscriptionUpdate(**data)


class AzureEventGridDestinationSchema(DestinationSchema):
    "Marshmallow schema for :class:`commercetools.types.AzureEventGridDestination`."
    uri = marshmallow.fields.String(allow_none=True)
    access_key = marshmallow.fields.String(allow_none=True, data_key="accessKey")

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type"]
        return types.AzureEventGridDestination(**data)


class AzureServiceBusDestinationSchema(DestinationSchema):
    "Marshmallow schema for :class:`commercetools.types.AzureServiceBusDestination`."
    connection_string = marshmallow.fields.String(
        allow_none=True, data_key="connectionString"
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type"]
        return types.AzureServiceBusDestination(**data)


class DeliveryCloudEventsFormatSchema(DeliveryFormatSchema):
    "Marshmallow schema for :class:`commercetools.types.DeliveryCloudEventsFormat`."
    cloud_events_version = marshmallow.fields.String(
        allow_none=True, data_key="cloudEventsVersion"
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type"]
        return types.DeliveryCloudEventsFormat(**data)


class DeliveryPlatformFormatSchema(DeliveryFormatSchema):
    "Marshmallow schema for :class:`commercetools.types.DeliveryPlatformFormat`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type"]
        return types.DeliveryPlatformFormat(**data)


class GoogleCloudPubSubDestinationSchema(DestinationSchema):
    "Marshmallow schema for :class:`commercetools.types.GoogleCloudPubSubDestination`."
    project_id = marshmallow.fields.String(allow_none=True, data_key="projectId")
    topic = marshmallow.fields.String(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type"]
        return types.GoogleCloudPubSubDestination(**data)


class IronMqDestinationSchema(DestinationSchema):
    "Marshmallow schema for :class:`commercetools.types.IronMqDestination`."
    uri = marshmallow.fields.String(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type"]
        return types.IronMqDestination(**data)


class MessageDeliverySchema(SubscriptionDeliverySchema):
    "Marshmallow schema for :class:`commercetools.types.MessageDelivery`."
    id = marshmallow.fields.String(allow_none=True)
    version = marshmallow.fields.Integer(allow_none=True)
    created_at = marshmallow.fields.DateTime(allow_none=True, data_key="createdAt")
    last_modified_at = marshmallow.fields.DateTime(
        allow_none=True, data_key="lastModifiedAt"
    )
    sequence_number = marshmallow.fields.Integer(
        allow_none=True, data_key="sequenceNumber"
    )
    resource_version = marshmallow.fields.Integer(
        allow_none=True, data_key="resourceVersion"
    )
    payload_not_included = marshmallow.fields.Nested(
        nested="commercetools.schemas._subscription.PayloadNotIncludedSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        data_key="payloadNotIncluded",
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["notification_type"]
        return types.MessageDelivery(**data)


class ResourceCreatedDeliverySchema(SubscriptionDeliverySchema):
    "Marshmallow schema for :class:`commercetools.types.ResourceCreatedDelivery`."
    version = marshmallow.fields.Integer(allow_none=True)
    modified_at = marshmallow.fields.DateTime(allow_none=True, data_key="modifiedAt")

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["notification_type"]
        return types.ResourceCreatedDelivery(**data)


class ResourceDeletedDeliverySchema(SubscriptionDeliverySchema):
    "Marshmallow schema for :class:`commercetools.types.ResourceDeletedDelivery`."
    version = marshmallow.fields.Integer(allow_none=True)
    modified_at = marshmallow.fields.DateTime(allow_none=True, data_key="modifiedAt")

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["notification_type"]
        return types.ResourceDeletedDelivery(**data)


class ResourceUpdatedDeliverySchema(SubscriptionDeliverySchema):
    "Marshmallow schema for :class:`commercetools.types.ResourceUpdatedDelivery`."
    version = marshmallow.fields.Integer(allow_none=True)
    old_version = marshmallow.fields.Integer(allow_none=True, data_key="oldVersion")
    modified_at = marshmallow.fields.DateTime(allow_none=True, data_key="modifiedAt")

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["notification_type"]
        return types.ResourceUpdatedDelivery(**data)


class SnsDestinationSchema(DestinationSchema):
    "Marshmallow schema for :class:`commercetools.types.SnsDestination`."
    access_key = marshmallow.fields.String(allow_none=True, data_key="accessKey")
    access_secret = marshmallow.fields.String(allow_none=True, data_key="accessSecret")
    topic_arn = marshmallow.fields.String(allow_none=True, data_key="topicArn")

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type"]
        return types.SnsDestination(**data)


class SqsDestinationSchema(DestinationSchema):
    "Marshmallow schema for :class:`commercetools.types.SqsDestination`."
    access_key = marshmallow.fields.String(allow_none=True, data_key="accessKey")
    access_secret = marshmallow.fields.String(allow_none=True, data_key="accessSecret")
    queue_url = marshmallow.fields.String(allow_none=True, data_key="queueUrl")
    region = marshmallow.fields.String(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type"]
        return types.SqsDestination(**data)


class SubscriptionChangeDestinationActionSchema(SubscriptionUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.SubscriptionChangeDestinationAction`."
    destination = helpers.Discriminator(
        discriminator_field=("type", "type"),
        discriminator_schemas={
            "EventGrid": "commercetools.schemas._subscription.AzureEventGridDestinationSchema",
            "AzureServiceBus": "commercetools.schemas._subscription.AzureServiceBusDestinationSchema",
            "GoogleCloudPubSub": "commercetools.schemas._subscription.GoogleCloudPubSubDestinationSchema",
            "IronMQ": "commercetools.schemas._subscription.IronMqDestinationSchema",
            "SNS": "commercetools.schemas._subscription.SnsDestinationSchema",
            "SQS": "commercetools.schemas._subscription.SqsDestinationSchema",
        },
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.SubscriptionChangeDestinationAction(**data)


class SubscriptionSetChangesActionSchema(SubscriptionUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.SubscriptionSetChangesAction`."
    changes = marshmallow.fields.Nested(
        nested="commercetools.schemas._subscription.ChangeSubscriptionSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
        missing=None,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.SubscriptionSetChangesAction(**data)


class SubscriptionSetKeyActionSchema(SubscriptionUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.SubscriptionSetKeyAction`."
    key = marshmallow.fields.String(allow_none=True, missing=None)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.SubscriptionSetKeyAction(**data)


class SubscriptionSetMessagesActionSchema(SubscriptionUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.SubscriptionSetMessagesAction`."
    messages = marshmallow.fields.Nested(
        nested="commercetools.schemas._subscription.MessageSubscriptionSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
        missing=None,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.SubscriptionSetMessagesAction(**data)
