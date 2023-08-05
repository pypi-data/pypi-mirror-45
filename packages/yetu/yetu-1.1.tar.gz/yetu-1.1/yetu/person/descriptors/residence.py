"""
location/Citizen/Residence related information  Descriptors
"""

__author__ = 'David Johnnes'
__email__ = "david.johnnes@gmail.com"


class CountryOfBirth:
    """"""
    def __init__(self, country_name=None, max_len=30):
        self.name = country_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The CountryOfBirth must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of CountryOfBirth must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "country_of_birth"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class StateOfBirth:
    """"""
    def __init__(self, state_name=None, max_len=30):
        self.name = state_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The StateOfBirth must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of StateOfBirth must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "state_of_birth"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class VillageOfBirth:
    """"""
    def __init__(self, village_name=None, max_len=30):
        self.name = village_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The VillageOfBirth must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of VillageOfBirth must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "village_of_birth"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class TownOfBirth:
    """"""
    def __init__(self, town_name=None, max_len=30):
        self.name = town_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The TownOfBirth must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of TownOfBirth must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "town_of_birth"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class YearOfBirth:
    """"""
    def __init__(self, year_of_birth=None, max_len=30):
        self.name = year_of_birth
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The YearOfBirth must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of YearOfBirth must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "year_of_birth"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class DayOfBirth:
    """"""
    def __init__(self, day_of_birth=None, max_len=30):
        self.name = day_of_birth
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The DayOfBirth must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of DayOfBirth must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "day_of_birth"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class MonthOfBirth:
    """"""
    def __init__(self, month_of_birth=None, max_len=30):
        self.name = month_of_birth
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The MonthOfBirth must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of MonthOfBirth must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "month_of_birth"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class ContinentOfBirth:
    """"""
    def __init__(self, continent_of_birth=None, max_len=30):
        self.name = continent_of_birth
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The ContinentOfBirth must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of ContinentOfBirth must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "continent_of_birth"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class MotherTongue:
    """"""
    def __init__(self, mother_tongue=None, max_len=30):
        self.name = mother_tongue
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The MotherTongue must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of MotherTongue must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "mother_tongue"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class IsPolyglot:
    """"""
    def __init__(self, value=None):
        self.name = value

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The value of Is_polyglot must be a bool!")

        if not self.name:
            self.name = "is_polyglot"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class CountryOfResidence:
    """"""
    def __init__(self, country_of_residence=None, max_len=30):
        self.name = country_of_residence
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The CountryOfResidence must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of CountryOfResidence must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "country_of_residence"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class StateOfResidence:
    """"""
    def __init__(self, state_of_residence=None, max_len=30):
        self.name = state_of_residence
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The StateOfResidence must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of StateOfResidence must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "state_of_residence"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class AddressOfResidence:
    """"""
    def __init__(self, address_of_residence=None, max_len=30):
        self.name = address_of_residence
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The AddressOfResidence must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of AddressOfResidence must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "address_of_residence"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class PermitType:
    """"""
    def __init__(self, permit_type=None, max_len=30):
        self.name = permit_type
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The PermitType must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of PermitType must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "permit_type"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class IsResident:
    """"""
    def __init__(self, value=None):
        self.name = value

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise AttributeError("The value of IsResident must be a bool!")

        if not self.name:
            self.name = "is_resident"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class IsCitizen:
    """"""
    def __init__(self, value=None):
        self.name = value

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise AttributeError("The value of IsResident must be a bool!")

        if not self.name:
            self.name = "is_citizen"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class StreetOfResidence:
    """"""
    def __init__(self, street_of_residence=None, max_len=30):
        self.name = street_of_residence
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The StreetOfResidence must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of StreetOfResidence must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "street_of_residence"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]










































