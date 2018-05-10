import yaml

from shared.models import Person

# TODO: Make environment variable
blurb_dictionary: dict = yaml.load("blurbs.yaml")

def build_message(person: Person) -> str:
    message = ""

    if person.company.lower() != 'microsoft':
        raise NotImplementedError
    else:
        message += blurb_dictionary.get('intro') + \
                   blurb_dictionary.get(person.company.lower()) + \
                   blurb_dictionary.get('outro')
        message.format(name=person.name, company=person.company)
        print(message)

    assert len(message) < 300

    return message