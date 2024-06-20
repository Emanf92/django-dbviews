from functools import partial
from typing import List, Type, Union

from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps


formatted_queries_registry = {}


def view_of(models: List[Union[Type[Model], str]], query: str):
    def wrapper(view_model: Type[Model]) -> Type[Model]:
        for source_model in models:
            receiver(post_save, sender=source_model)(partial(view_binder, view_model, query, models))
        return view_model

    return wrapper


def ensure_models(models: List[Union[Type[Model], str]]) -> List[Type[Model]]:
    return [
        (model if isinstance(model, Model) else apps.get_model(*model.split(".", 2)))
        for model in models
    ]


def format_query(query: str, models: List[Type[Model]]) -> str:
    query_key = f"{query}/{models}"
    if query_key not in formatted_queries_registry:
        db_models = ensure_models(models)
        for index, model in enumerate(db_models, 1):
            query = query.replace(f"${index}", str(model._meta.db_table))

        formatted_queries_registry[query_key] = query

    return formatted_queries_registry[query_key]


def view_binder(view_model: Type[Model], query: str, source_models, *args, **kwargs):
    formatted_query = format_query(query, source_models)
    view_items = view_model.objects.raw(formatted_query)
    [item.save() for item in view_items]
