import json
import re
from typing import get_args

from pydantic import BaseModel


def schema_to_example(
    model: type[BaseModel], omit_fields: list[str] | None = None
) -> str:
    """Convert a Pydantic model to a JSON example string with comments."""
    if omit_fields is None:
        omit_fields = []

    def _inner(model: type[BaseModel]):
        """Recursively build example dict and description map from Pydantic model."""
        example = {}
        descriptions = {}

        for field_name, field_info in model.model_fields.items():
            annotation = field_info.annotation
            if field_name in omit_fields:
                continue
            descriptions[field_name] = f"  # {field_info.description}"

            if isinstance(annotation, type) and issubclass(annotation, BaseModel):
                nested_example, nested_desc = _inner(annotation)
                example[field_name] = nested_example
                # prefix nested descriptions with parent field
                for k, v in nested_desc.items():
                    descriptions[f"{field_name}.{k}"] = v
            else:
                example[field_name] = (
                    annotation.__name__
                    if isinstance(annotation, type) and not any(get_args(annotation))
                    else str(annotation)
                )

        return example, descriptions

    def _insert_comments(schema_json: str, descriptions: dict):
        """Insert comments in JSON string output based on dot-paths in `descriptions`."""
        for field_path, comment in sorted(
            descriptions.items(), key=lambda x: -x[0].count(".")
        ):
            # Build regex to match the specific line for that field
            parts = field_path.split(".")
            last_key = parts[-1]
            pattern = rf'^(\s*)"{last_key}": .*$'
            schema_json = re.sub(
                pattern,
                lambda m: m.group(0) + comment,  # noqa
                schema_json,
                count=1,
                flags=re.MULTILINE,
            )
        return schema_json

    example, descriptions = _inner(model)
    schema_json = json.dumps(example, indent=2)
    schema_json_annotations_non_strings = re.sub(
        r'(":[ ]*)"([^"]+)"', r"\1\2", schema_json
    )
    schema_with_comments = _insert_comments(
        schema_json_annotations_non_strings, descriptions
    )
    return schema_with_comments
