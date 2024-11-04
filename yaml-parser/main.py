class YamlParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.parsed_data = None

    def load_and_parse(self):
        with open(self.file_path, 'r') as file:
            content = file.read()
            self.parsed_data = self._parse_content(content.splitlines())

    def _parse_content(self, lines, indent_level=0):
        result = {}
        current_key = None

        while lines:
            line = lines.pop(0).rstrip()
            if not line or line.startswith("#"):  # Ignorer les lignes vides et les commentaires
                continue

            # Calculer le niveau d'indentation de la ligne actuelle
            current_indent = len(line) - len(line.lstrip())
            if current_indent < indent_level:
                # Fin de la structure imbriquée actuelle
                lines.insert(0, line)  # Remettre la ligne pour le niveau suivant
                break

            line = line.lstrip()
            if line.startswith('- '):  # Gérer les éléments de liste
                line_content = line[2:]
                # Si aucun `current_key` n'est défini, on est dans une liste de niveau supérieur
                if current_key is None:
                    if not isinstance(result, list):
                        result = []
                    result.append(self._parse_value(line_content, lines, current_indent + 2))
                else:
                    # Initialiser une liste pour `current_key` si non déjà fait
                    if not isinstance(result[current_key], list):
                        result[current_key] = []
                    result[current_key].append(self._parse_value(line_content, lines, current_indent + 2))

            elif ":" in line:  # Gérer les paires clé-valeur ou les structures imbriquées
                # Diviser seulement sur le premier ":", pour permettre les deux-points dans les valeurs
                key, value = line.split(":", 1)
                current_key = key.strip()
                value = value.strip()

                # Vérifier si la valeur est vide, indiquant une structure imbriquée
                if not value:
                    result[current_key] = self._parse_content(lines, current_indent + 2)
                else:
                    result[current_key] = self._parse_value(value, lines, current_indent + 2)

            else:
                raise ValueError(f"Format YAML invalide à la ligne : {line}")

        return result

    def _parse_value(self, value, lines, indent_level):
        if not value:
            return self._parse_content(lines, indent_level)
        elif value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit():
            return float(value)
        elif value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        else:
            return value

    def get_parsed_data(self):
        return self.parsed_data


if __name__ == "__main__":
    parser = YamlParser('yaml_demo.yaml')
    parser.load_and_parse()
    print(parser.get_parsed_data())
