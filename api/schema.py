from graphene import Schema, ObjectType, Mutation, ID, Int, String, List, JSONString, Field
import neomodels

# SCHEMA
class GroupType(ObjectType):
    id_1 = ID()
    id_2 = ID()
    code = String()
    name = String()
    validity = String()
    geometry = JSONString()
    level = String()

    countries = List(lambda: CountryType)

    @staticmethod
    def resolve_countries(parent, info):
        
        group = neomodels.Group.nodes.first_or_none(name=parent['name'])
        return [c.__properties__ for c in group.countries]
    
class CountryType(ObjectType):
    id_1 = ID()
    id_2 = ID()
    code = String()
    name = String()
    validity = String()
    geometry = JSONString()
    level = String()

    group = Field(GroupType)
    regions = List(lambda: RegionType)

    @staticmethod
    def resolve_group(parent, info):
        country = neomodels.Country.nodes.first_or_none(name=parent['name'])
        return country.group[0].__properties__

    @staticmethod
    def resolve_regions(parent, info):
        country = neomodels.Country.nodes.first_or_none(name=parent['name'])
        return [r.__properties__ for r in country.regions]

class RegionType(ObjectType):
    
    id_1 = ID()
    id_2 = ID()
    code = String()
    name = String()
    validity = String()
    geometry = JSONString()
    level = String()

    country = Field(CountryType)
    departements = List(lambda: DepartementType)

    @staticmethod
    def resolve_country(parent, info):
        region = neomodels.Region.nodes.first_or_none(name=parent['name'])
        return region.country[0].__properties__
    
    @staticmethod
    def resolve_departements(parent, info):
        region = neomodels.Region.nodes.first_or_none(name=parent['name'])
        return [r.__properties__ for r in region.departements]

class DepartementType(ObjectType):

    id_1 = ID()
    id_2 = ID()
    code = String()
    name = String()
    validity = String()
    geometry = JSONString()
    level = String()

    region = Field(RegionType)
    communes = List(lambda: RegionType)

    @staticmethod
    def resolve_region(parent, info):
        departement = neomodels.Departement.nodes.first_or_none(name=parent['name'])
        return departement.region[0].__properties__

    @staticmethod
    def resolve_communes(parent, info):
        departement = neomodels.Departement.nodes.first_or_none(name=parent['name'])
        return [r.__properties__ for r in departement.communes]

class CommuneType(ObjectType):

    id_1 = ID()
    id_2 = ID()
    code = String()
    name = String()
    validity = String()
    geometry = JSONString()
    level = String()

    departemnt = Field(CountryType)
    users = List(lambda: UserType)

    @staticmethod
    def resolve_departement(parent, info):
        commune = neomodels.Commune.nodes.first_or_none(name=parent['name'])
        return commune.departement[0].__properties__

    @staticmethod
    def resolve_communes(parent, info):
        commune = neomodels.Commune.nodes.first_or_none(name=parent['name'])
        return [r.__properties__ for r in commune.users]

class UserType(ObjectType):
    id = ID()
    username = String()
    email = String()
    password = String()
    party = String()
    commune = Field(CommuneType)

    @staticmethod
    def resolve_commune(parent, info):
        user = neomodels.User.nodes.first_or_none(name=parent['name'])
        return user.commune[0].__properties__

# QUERY

class Query(ObjectType):

    # Group 
    groups = List(GroupType)
    def resolve_groups(parent, info):
        return [g.__properties__ for g in neomodels.Group.nodes.all()]
    
    group = Field(GroupType, name=String())
    def resolve_group(parent, info, name: str):
        group = neomodels.Group.nodes.first_or_none(name=name)
        return group.__properties__
    
    # Country
    countries = List(CountryType)
    def resolve_countries(parent, info):
        return [c.__properties__ for c in neomodels.Country.nodes.all()]
    
    country = Field(CountryType, name=String())
    def resolve_country(parent, info, name: str):
        country = neomodels.Country.nodes.first_or_none(name=name)
        return country.__properties__
   

    # Region
    regions = List(RegionType)
    def resolve_regions(parent, info):        
        return [c.__properties__ for c in neomodels.Region.nodes.all()]

    region = Field(RegionType, name=String())
    def resolve_region(parent, info, name: str):
        region = neomodels.Region.nodes.first_or_none(name=name)
        return region.__properties__

    # Departement

    departements = List(DepartementType)
    def resolve_departements(parent, info):
        return [c.__properties__ for c in neomodels.Departement.nodes.all()]

    departement = Field(DepartementType, name=String())
    def resolve_departement(parent, info, name: str):
        departement = neomodels.Departement.nodes.first_or_none(name=name)
        return departement.__properties__

    # Commune

    communes = List(CommuneType)
    def resolve_communes(parent, info):
        return [c.__properties__ for c in neomodels.Commune.nodes.all()]

    commune = Field(CommuneType, name=String())
    def resolve_commune(parent, info, name: str):
        commune = neomodels.Commune.nodes.first_or_none(name=name)
        return commune.__properties__

    # User

    user = List(UserType)
    def resolve_user(parent, info):
        return [c.__properties__ for c in neomodels.User.nodes.all()]

# MUTATIONS

class CreateUser(Mutation):
    class Arguments:
        username = String()
        email = String()
        password = String()
        party = String()
        commune = String()

    user = Field(UserType)

    @staticmethod
    def mutate(parent, info, username, email, password, party, commune):
        user = neomodels.User(username=username, email=email, password=password, party=party)
        commune = neomodels.Commune.nodes.first_or_none(name=commune)
        user.save()
        user.commune.connect(commune)
        commune.users.connect(user)
        commune.save()
        user = user.__properties__
        return CreateUser(user=user) # user # CreateUser(user=user) # , username=username, email=email, password=password, party=party, commune=commune

class DeleteUser(Mutation):
    class Arguments:
        username = String()
    
    user = Field(UserType)

    @staticmethod
    def mutate(parent, info, username):
        user = neomodels.User.nodes.first_or_none(username=username) 
        user.commune.disconnect_all()
        user.delete()
        return DeleteUser(user=user)

class UpdateUser(Mutation):
    class Arguments:
        username = String()
        new_username = String()
    
    user = Field(UserType)

    @staticmethod
    def mutate(parent, info, username, new_username):
        user = neomodels.User.nodes.first_or_none(username=username) 
        user.username = new_username
        user.save()
        return UpdateUser(user=user)


class Mutations(ObjectType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    update_user = UpdateUser.Field()

schema=Schema(query=Query, mutation=Mutations)