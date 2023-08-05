from yetu.person.descriptors import person

__author__ = 'David Johnnes'
__email__ = "david.johnnes@gmail.com"


class Base(type):
    """Create custom meta-class for person"""

    def __new__(cls, name, bases, dict):
        """ """

        __new = super().__new__(cls, name, bases, dict)

        __new.first_name = person.FirstName()
        __new.middle_name = person.MiddleName()
        __new.last_name = person.LastName()
        __new.second_name = person.SecondName()
        __new.age = person.Age()
        __new.id = person.Id()
        __new.nick_name = person.NickName()
        __new.given_name = person.GivenName()
        __new.family_name = person.FamilyName()
        __new.sur_name = person.SurName()
        __new.civil_status = person.CivilStatus()
        __new.is_married = person.IsMarried()
        __new.is_single = person.IsSingle()
        __new.is_divorced = person.IsDivorced()
        __new.is_widowed = person.IsWidowed()
        __new.date_of_birth = person.DateOfBirth()
        __new.salary = person.Salary()
        __new.profession = person.Profession()
        __new.is_un_employed = person.IsUnEmployed()
        __new.is_employed = person.IsEmployed()
        __new.employer_name = person.EmployerName()
        __new.place_of_birth = person.PlaceOfBirth()
        return __new


class Person(metaclass=Base):
    """"""
    pass


















