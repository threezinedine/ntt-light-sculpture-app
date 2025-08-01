import os
from typing import Any, Dict
from jinja2 import FileSystemLoader, Template, Environment


class AutoGenTemplate:
    """
    The wrapper for the jinja2 template engine. The input is the template file.
    The template file is a jinja2 template file.

    Example:
    ```python
    template = Template("template.jinja2")
    result = template.render(name="John", age=30)
    print(result) # "Hello, John! You are 30 years old."

    template = Template("template-non-existing.jinja2") # will raise an error
    ```
    """

    def __init__(self, template_file) -> None:
        template_dir = os.path.dirname(template_file)
        file_name = os.path.basename(template_file)

        try:
            self._env = Environment(loader=FileSystemLoader(template_dir))
            self._template = self._env.get_template(file_name)
        except Exception as e:
            raise RuntimeError(f"Error loading template named '{file_name}': {e}")

    def render(self, data: Dict[str, Any]) -> str:
        """
        Receives a dictionary of data and renders the template.

        Return the rendered template as a string.
        """
        try:
            return self._template.render(**data)
        except Exception as e:
            raise RuntimeError(f"Error rendering template: {e}")
