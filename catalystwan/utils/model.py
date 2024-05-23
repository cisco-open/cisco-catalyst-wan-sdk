from inspect import isclass
from typing import Any, List, OrderedDict, Type, Union

from pydantic import BaseModel
from typing_extensions import Annotated, get_args, get_origin


def resolve_nested_base_model_unions(
    annotation: Any, models_types: List[Type[BaseModel]] = list()
) -> List[Type[BaseModel]]:
    """given something like AnyParcel produces flat list of BaseModel sub-types present in that union

    Args:
        annotation (Any): Union of BaseModels (could be Annotated and nested)
        models_types (List[Type[BaseModel]], optional): used internally in recurence

    Raises:
        TypeError: when contents are not BaseModel (can be Annotated)

    Returns:
        List[Type[BaseModel]]: flat list of subclasses of BaseModel present in input
    """

    models_types = list(OrderedDict.fromkeys(models_types))

    if isclass(annotation):
        if issubclass(annotation, BaseModel):
            return [annotation]
        raise TypeError()

    type_origin = get_origin(annotation)
    # Check if Annnotated[Union[PayloadModelType, ...]], only unions of pydantic models allowed
    if type_origin == Annotated:
        if annotated_origin := get_args(annotation):
            if len(annotated_origin) >= 1:
                origin = annotated_origin[0]
                if isclass(origin) and issubclass(origin, BaseModel):
                    return [origin]
                if get_origin(origin) == Union:
                    type_args = get_args(origin)
                    if all(isclass(t) for t in type_args) and all(issubclass(t, BaseModel) for t in type_args):
                        models_types.extend(list(type_args))
                        return models_types
                    else:
                        non_models = [t for t in type_args if not isclass(t)]
                        for non_model in non_models:
                            models_types.extend(resolve_nested_base_model_unions(non_model, models_types))
                        return models_types

    # Check if Union[PayloadModelType, ...], only unions of pydantic models allowed
    elif type_origin == Union:
        type_args = get_args(annotation)
        if all(isclass(t) for t in type_args) and all(issubclass(t, BaseModel) for t in type_args):
            models_types.extend(list(type_args))
            return models_types
        else:
            non_models = [t for t in type_args if not isclass(t)]
            for non_model in non_models:
                models_types.extend(resolve_nested_base_model_unions(non_model, models_types))
            return models_types
    raise TypeError()
