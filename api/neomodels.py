from neomodel import StructuredNode, RelationshipTo, RelationshipFrom, UniqueIdProperty, StringProperty, JSONProperty, DateTimeProperty

class Admin(StructuredNode):
    __abstract_node__ = True

    id_1 = UniqueIdProperty()
    id_2 = UniqueIdProperty()
    code = UniqueIdProperty()	
    name = StringProperty(required = True)	
    validity = DateTimeProperty()
    geometry = JSONProperty(required = True)	
    level = StringProperty(required = True)	


class World(Admin):
    groups = RelationshipTo('Group', 'GROUP')
    countries = RelationshipTo('Country', 'COUNTRY')

class Group(Admin):
    world = RelationshipFrom('World', 'Group')

    countries = RelationshipTo('Country', 'COUNTRY')

class Country(Admin):
    group = RelationshipFrom('Group', "COUNTRY")
    world = RelationshipFrom('World', "COUNTRY")

    regions = RelationshipTo('Region', 'REGION')
    collectivites = RelationshipTo('Collectivite', 'COLLECTIVITE')

class Collectivite(Admin):
    country = RelationshipFrom('Country', "COLLECTIVITE")

class Region(Admin):
    country = RelationshipFrom('Country', 'REGION')

    departements = RelationshipTo('Departement', 'DEPARTEMENT')

class Subset(Admin):
    departements = RelationshipTo('Departement', 'DEPARTEMENT')
    
class Departement(Admin):
    subset = RelationshipFrom('Subset', 'DEPARTEMENT')
    region = RelationshipFrom('Region', 'DEPARTEMENT')

    communes = RelationshipTo('Commune', 'COMMUNE')

class Epci(Admin):
    communes = RelationshipTo('Commune', 'COMMUNE')
    
class Arrondissement(Admin):
    communes = RelationshipTo('Commune', 'COMMUNE')

class Commune(Admin):
    departement = RelationshipFrom('Departement', 'COMMUNE')
    arrondissement = RelationshipFrom('Arrondissement', 'COMMUNE')
    epci = RelationshipFrom('Epci', 'COMMUNE')

    users = RelationshipTo('User', 'USER')

class User(StructuredNode):
    id_1 = UniqueIdProperty()
    id_2 = UniqueIdProperty()
    username = StringProperty(required=True, unique_index=True)
    email = StringProperty(required=True, unique_index=True)
    password = StringProperty(required=True, unique_index=True)
    party = StringProperty()
