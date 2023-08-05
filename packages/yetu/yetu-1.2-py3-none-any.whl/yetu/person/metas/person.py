from yetu.person.descriptors import person
from yetu.person.descriptors import residence


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

        # =========================residence descriptors==================================================
        __new.country_of_birth = residence.ContinentOfBirth()
        __new.state_of_birth = residence.StateOfBirth()
        __new.village_of_birth = residence.VillageOfBirth()
        __new.town_of_birth = residence.TownOfBirth()
        __new.year_of_birth = residence.YearOfBirth()
        __new.day_of_birth = residence.DayOfBirth()
        __new.month_of_birth = residence.MonthOfBirth()
        __new.continent_of_birth = residence.ContinentOfBirth()
        __new.mother_tongue = residence.MotherTongue()
        __new.is_polyglot = residence.IsPolyglot()
        __new.country_of_residence = residence.CountryOfResidence()
        __new.state_of_residence = residence.StateOfResidence()
        __new.address_of_residence = residence.AddressOfResidence()
        __new.permit_type = residence.PermitType()
        __new.is_resident = residence.IsResident()
        __new.is_citizen = residence.IsCitizen()
        __new.street_of_residence = residence.StreetOfResidence()
        return __new


class Person(metaclass=Base):
    """"""
    pass




















