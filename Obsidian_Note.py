# Obsidian_Note.py


from Molecule import Molecule
from typing import Any
import yaml


# TODO: docstring
class Obsidian_Note(Molecule):
    @staticmethod
    def parse_YAML_and_body_from_Markdown(
        Markdown_file_path: str,
    ) -> tuple[dict[str, Any], str]:
        Markdown_file_YAML = dict()
        with open(Markdown_file_path, 'r') as Markdown_file:
            if (Markdown_file_content := Markdown_file.read()).startswith('---\n'):
                if len(Markdown_file_parts := Markdown_file_content.split('---\n', 2)[1:]) == 2:
                    # TODO: make this intelligently remove only one newline so the body text is accurate and then warn if there isn't one since that would violate what Obsidian expects
                    Markdown_file_frontmatter: str = Markdown_file_parts[0][:-1]
                    Markdown_file_YAML = yaml.safe_load(Markdown_file_frontmatter) #type:ignore
                    if type(Markdown_file_YAML) is not dict:
                        raise ValueError(f"Invalid YAML {Markdown_file_YAML}")
                    Markdown_file_YAML = {str(key): value for key, value in Markdown_file_YAML.items()}
                    Markdown_file_body = Markdown_file_parts[1]
                else:
                    Markdown_file_body = Markdown_file_content
            else:
                Markdown_file_body = Markdown_file_content
            return Markdown_file_YAML, Markdown_file_body


if __name__ == "__main__":
    print(Obsidian_Note().parse_YAML_and_body_from_Markdown("test.md"))
