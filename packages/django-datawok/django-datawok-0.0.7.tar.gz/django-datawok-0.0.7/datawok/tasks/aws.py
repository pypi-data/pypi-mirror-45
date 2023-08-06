import json
import os
import logging

from celery import shared_task

from datawok.models import datawok_models, Meta
from datawok.serializers import datawok_publish_serializers
from datawok.utils.aws import defaults, get_bucket
from django.utils import timezone

logger = logging.getLogger("tasks")


@shared_task(acks_late=True)
def publish_to_aws(model_name, filename="data.json", data=None):
    model = [
        model
        for model in datawok_models
        if model.__name__.lower() == model_name
    ][0]

    try:
        meta = Meta.objects.get(datawok_model__model=model_name)
    except Meta.DoesNotExist:
        return

    if not data:
        i = datawok_models.index(model)
        serializer = datawok_publish_serializers[i]
        data = json.dumps(serializer(model.objects.all(), many=True).data)

    key = os.path.join(meta.get_publish_path(), filename.lstrip("/"))

    bucket = get_bucket()

    bucket.put_object(
        Key=key,
        ACL=defaults.ACL,
        Body=data,
        CacheControl=defaults.CACHE_HEADER,
        ContentType="application/json",
    )

    logger.info("Published to AWS")

    meta.last_published = timezone.now()
    meta.save()

    logger.info("Updated meta last_published.")
