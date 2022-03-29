from escavador.institutions import Institutions
from escavador.persons import Persons
from escavador.credits import Credits
from escavador.journals import Journals
from escavador.court import Court
from escavador.motions import Motions
from escavador.async_search import AsyncSearch
import json

instituitions = Institutions()
persons = Persons()
credits = Credits()
journals = Journals()
court = Court()
motions = Motions()
async_lawsuit = AsyncSearch()
print((json.dumps(async_lawsuit.get_lawsuit("1075874-67.2020.8.26.0100"), indent=4)))