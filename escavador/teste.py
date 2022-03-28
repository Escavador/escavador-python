from escavador.institutions import Institutions
from escavador.persons import Persons
from escavador.credits import Credits
from escavador.journals import Journals
from escavador.court import Court
from escavador.motions import Motions
import json

instituitions = Institutions()
persons = Persons()
credits = Credits()
journals = Journals()
court = Court()
motions = Motions()
print((json.dumps(motions.get_motion(1), indent=4)))