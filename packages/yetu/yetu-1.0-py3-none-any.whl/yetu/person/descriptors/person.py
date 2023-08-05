"""
Person  Descriptors
"""

__author__ = 'David Johnnes'
__email__ = "david.johnnes@gmail.com"


class FirstName:
    """"""
    def __init__(self, first_name=None, max_len=30):
        self.name = first_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The FirstName must be a string!")

        if not value.isalpha():
            raise AttributeError("The FirstName must be alpha!")

        if len(value) > self.max_len:
            raise AttributeError("The length of FirstName must not be greater than {0}".format(self.max_len))
        if not self.name:
            self.name = "first_name"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class MiddleName:
    """"""
    def __init__(self, middle_name=None, max_len=30):
        self.name = middle_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The MiddleName must be a string!")

        if not value.isalpha():
            raise AttributeError("The MiddleName must be alpha!")

        if len(value) > self.max_len:
            raise AttributeError("The length of MiddleName must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "middle_name"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class LastName:
    """"""
    def __init__(self, last_name=None, max_len=30):
        self.name = last_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The LastName must be a string!")

        if not value.isalpha():
            raise AttributeError("The LastName must be alpha!")

        if len(value) > self.max_len:
            raise AttributeError("The length of LastName must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "last_name"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class SecondName:
    """"""
    def __init__(self, second_name=None, max_len=30):
        self.name = second_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The SecondName must be a string!")

        if not value.isalpha():
            raise AttributeError("The SecondName must be alpha!")

        if len(value) > self.max_len:
            raise AttributeError("The length of SecondName must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "second_name"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Age:
    """ """
    def __init__(self, age=None, max_age=150):
        self.age = age
        self.max_age = max_age

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.age)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise AttributeError("The Age must be an int!")

        if not value > 0:
            raise AttributeError("The Age must not be less than 1!")

        if value > self.max_age:
            raise AttributeError("The Age must not be greater than {0}".format(self.max_age))

        if not self.age:
            self.age = "age"

        instance.__dict__[self.age] = value


class Id:
    """ """
    def __init__(self, id=None, max_len=30):
        self.name = id
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The ID must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of ID must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "id"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class NickName:
    """"""
    def __init__(self, nick_name=None, max_len=30):
        self.name = nick_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The NickName must be a string!")

        if not value.isalpha():
            raise AttributeError("The NickName must be alpha!")

        if len(value) > self.max_len:
            raise AttributeError("The length of NickName must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "nick_name"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class GivenName:
    """"""
    def __init__(self, given_name=None, max_len=30):
        self.name = given_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The GivenName must be a string!")

        if not value.isalpha():
            raise AttributeError("The GivenName must be alpha!")

        if len(value) > self.max_len:
            raise AttributeError("The length of GivenName must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "given_name"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class FamilyName:
    """"""
    def __init__(self, family_name=None, max_len=30):
        self.name = family_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The FamilyName must be a string!")

        if not value.isalpha():
            raise AttributeError("The FamilyName must be alpha!")

        if len(value) > self.max_len:
            raise AttributeError("The length of FamilyName must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "family_name"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class SurName:
    """"""
    def __init__(self, sur_name=None, max_len=30):
        self.name = sur_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The SurName must be a string!")

        if not value.isalpha():
            raise AttributeError("The SurName must be alpha!")

        if len(value) > self.max_len:
            raise AttributeError("The length of SurName must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "sur_name"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class CivilStatus:
    """"""
    def __init__(self, civil_status=None, max_len=30):
        self.name = civil_status
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The CivilStatus must be a string!")

        if not value.isalpha():
            raise AttributeError("The CivilStatus must be alpha!")

        if len(value) > self.max_len:
            raise AttributeError("The length of CivilStatus must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "civil_status"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class IsMarried:
    """ """
    def __init__(self, status=None):
        self.value = status

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.value)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise AttributeError("The IsMarried  value must be a bool!")

        if not self.value:
            self.value = "is_married"
        instance.__dict__[self.value] = value


class IsSingle:
    """ """
    def __init__(self, status=None):
        self.value = status

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.value)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise AttributeError("The IsSingle  value must be a bool!")

        if not self.value:
            self.value = "is_single"

        instance.__dict__[self.value] = value


class IsDivorced:
    """ """
    def __init__(self, status=None):
        self.value = status

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.value)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise AttributeError("The IsDivorced  value must be a bool!")

        if not self.value:
            self.value = "is_divorced"
        instance.__dict__[self.value] = value


class IsWidowed:
    """ """
    def __init__(self, status=None):
        self.value = status

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.value)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise AttributeError("The IsWidowed  value must be a bool!")

        if not self.value:
            self.value = "is_widowed"

        instance.__dict__[self.value] = value


class DateOfBirth:
    """"""
    def __init__(self, date_of_birth=None, max_len=30):
        self.date_of_birth = date_of_birth
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.date_of_birth)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The DateOfBirth must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of DateOfBirth must not be greater than {0}".format(self.max_len))

        if not self.date_of_birth:
            self.date_of_birth = "date_of_birth"

        instance.__dict__[self.date_of_birth] = value

    def __delete__(self, instance):
        del instance.__dict__[self.date_of_birth]


class Salary:
    """"""
    def __init__(self, salary=None, max_value=20000.00):
        self.salary = salary
        self.max_len = max_value

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.salary)

    def __set__(self, instance, value):
        if not isinstance(value, float):
            raise AttributeError("The Salary must be a float!")

        if value > self.max_len:
            raise AttributeError("The Salary must not be greater than {0}".format(self.max_len))

        if not self.salary:
            self.salary = "salary"

        instance.__dict__[self.salary] = value

    def __delete__(self, instance):
        del instance.__dict__[self.salary]


class Profession:
    """"""
    def __init__(self, profession=None, max_len=30):
        self.name = profession
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The Profession must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of Profession must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "profession"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class IsUnEmployed:
    """ """
    def __init__(self, status=None):
        self.name = status

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise AttributeError("The IsUnEmployed status must be a bool!")

        if not self.name:
            self.name = "is_un_employed"
        instance.__dict__[self.name] = value


class IsEmployed:
    """ """
    def __init__(self, status=None):
        self.name = status

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise AttributeError("The IsEmployed status must be a bool!")

        if not self.name:
            self.name = "is_employed"

        instance.__dict__[self.name] = value


class EmployerName:
    """"""
    def __init__(self, employer_name=None, max_len=30):
        self.name = employer_name
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The EmployerName name must be a string!")

        if len(value) > self.max_len:
            raise AttributeError("The length of EmployerName name must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "employer"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class PlaceOfBirth:
    """"""
    def __init__(self, place_of_birth=None, max_len=30):
        self.name = place_of_birth
        self.max_len = max_len

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise AttributeError("The PlaceOfBirth must be a string! and not [{}]".format(type(value)))

        if len(value) > self.max_len:
            raise AttributeError("The length of PlaceOfBirth must not be greater than {0}".format(self.max_len))

        if not self.name:
            self.name = "place_of_birth"

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]












































