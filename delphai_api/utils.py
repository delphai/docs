from fastapi.routing import APIRoute
from pydantic import BaseModel


class HTTPExceptionModel(BaseModel):
    detail: str


def walk_dependency_tree(dependant, visited=None):
    if visited is None:
        visited = set()
    visited.add(dependant.cache_key)

    for sub_dependant in dependant.dependencies:
        if sub_dependant.cache_key in visited:
            continue

        yield sub_dependant
        yield from walk_dependency_tree(sub_dependant, visited)


def include_responses(app):
    @app.on_event("startup")
    def startup():
        for route in app.routes:
            if isinstance(route, APIRoute):
                for dependency in walk_dependency_tree(route.dependant):
                    dependency_responses = getattr(dependency.call, "responses", None)
                    if dependency_responses:
                        route.responses = dict(dependency_responses, **route.responses)

                endpoint_responses = getattr(route.endpoint, "responses", None)
                if endpoint_responses:
                    route.responses = dict(endpoint_responses, **route.responses)


def returns_errors(*error_codes):
    responses = {
        str(error_code): {"model": HTTPExceptionModel} for error_code in error_codes
    }

    def decorator(func):
        original_responses = getattr(func, "responses", {})
        func.responses = dict(original_responses, **responses)
        return func

    return decorator
