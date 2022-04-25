from escavador import Instituicao
import json

print(json.dumps(Instituicao().get(2),indent=2))