from yetu.person.metas.person import Person


__author__ = 'David Johnnes'
__email__ = "david.johnnes@gmail.com"


class PersonMethods(Person):
    """"""

    def set_first_name(self, new):
        self.first_name = new

    def get_first_name(self):
        return self.first_name

    def show_first_name(self):
        print(self.first_name)

    #  ============End Of FirstName=======================

    def set_middle_name(self, new):
        self.middle_name = new

    def get_middle_name(self):
        return self.middle_name

    def show_middle_name(self):
        print(self.middle_name)
    #  ============End Of MiddleName=======================

    def set_last_name(self, new):
        self.last_name = new

    def get_last_name(self):
        return self.last_name

    def show_last_name(self):
        print(self.last_name)
    #  ============End Of LastName=======================

    def set_second_name(self, new):
        self.second_name = new

    def get_second_name(self):
        return self.second_name

    def show_second_name(self):
        print(self.second_name)
    #  ============End Of SecondName=======================

    def show_fullname(self):
        """Shows only first name and last name as fullname"""
        print("{} {}".format(self.first_name, self.last_name))

    #  ============End Of Full name=======================

    def set_age(self, new):
        self.age = new

    def get_age(self):
        return self.age

    def show_age(self):
        print(self.age)
    #  ============End Of age===============================

    def set_id(self, new):
        self.id = new

    def get_id(self):
        return self.id

    def show_id(self):
        print(self.id)
    #  ============End Of Id===============================

    def set_nick_name(self, new):
        self.nick_name = new

    def get_nick_name(self):
        return self.nick_name

    def show_nick_name(self):
        print(self.nick_name)
    #  ============End Of Nick Name========================

    def set_given_name(self, new):
        self.given_name = new

    def get_given_name(self):
        return self.given_name

    def show_given_name(self):
        print(self.given_name)
    #  ============End Of Given Name=======================

    def set_family_name(self, new):
        self.family_name = new

    def get_family_name(self):
        return self.family_name

    def show_family_name(self):
        print(self.family_name)
    #  ============End Of Family Name======================

    def set_sur_name(self, new):
        self.sur_name = new

    def get_sur_name(self):
        return self.sur_name

    def show_sur_name(self):
        print(self.sur_name)
    #  ============End Of Sur Name=========================

    def set_civil_status(self, new):
        self.civil_status = new

    def get_civil_status(self):
        return self.civil_status

    def show_civil_status(self):
        print(self.civil_status)
    #  ============End Of Civil Status===============================

    def set_is_married(self, new):
        self.is_married = new

    def get_is_married(self):
        return self.is_married

    def show_is_married(self):
        print(self.is_married)
    #  ============End Of Is Married===============================

    def set_is_single(self, new):
        self.is_single = new

    def get_is_single(self):
        return self.is_single

    def show_is_single(self):
        print(self.is_single)
    #  ============End Of Is Single===============================

    def set_is_divorced(self, new):
        self.is_divorced = new

    def get_is_divorced(self):
        return self.is_divorced

    def show_is_divorced(self):
        print(self.is_divorced)
    #  ============End Of Is Divorced===============================

    def set_is_widowed(self, new):
        self.is_widowed = new

    def get_is_widowed(self):
        return self.is_widowed

    def show_is_widowed(self):
        print(self.is_widowed)
    #  ============End Of Is Widowed===============================

    def set_date_of_birth(self, new):
        self.date_of_birth = new

    def get_date_of_birth(self):
        return self.date_of_birth

    def show_date_of_birth(self):
        print(self.date_of_birth)
    #  ============End Of Date Of Birth===============================

    def set_salary(self, new):
        self.salary = new

    def get_salary(self):
        return self.salary

    def show_salary(self):
        print(self.salary)
    #  ============End Of Salary===============================

    def set_profession(self, new):
        self.profession = new

    def get_profession(self):
        return self.profession

    def show_profession(self):
        print(self.profession)
    #  ============End Of Profession===============================

    def set_is_un_employed(self, new):
        self.is_un_employed = new

    def get_is_un_employed(self):
        return self.is_un_employed

    def show_is_un_employed(self):
        print(self.is_un_employed)
    #  ============End Of Is Un Employed===============================

    def set_is_employed(self, new):
        self.is_employed = new

    def get_is_employed(self):
        return self.is_employed

    def show_is_employed(self):
        print(self.is_employed)
    #  ============End Of Is Employed===============================

    def set_employer_name(self, new):
        self.employer_name = new

    def get_employer_name(self):
        return self.employer_name

    def show_employer_name(self):
        print(self.employer_name)
    #  ============End Of Employer Name===============================

    def set_place_of_birth(self, new):
        self.place_of_birth = new

    def get_place_of_birth(self):
        return self.place_of_birth

    def show_place_of_birth(self):
        print(self.place_of_birth)
    #  ============End Of Place OF Birth===============================

#   Residence Methods
#   Residence Methods
    def set_country_of_birth(self, new):
        self.country_of_birth = new

    def get_country_of_birth(self):
        return self.country_of_birth

    def show_country_of_birth(self):
        print(self.country_of_birth)
    #  ============country_of_birth===============================

    def set_state_of_birth(self, new):
        self.state_of_birth = new

    def get_state_of_birth(self):
        return self.state_of_birth

    def show_state_of_birth(self):
        print(self.state_of_birth)
    #  ============state_of_birth===============================

    def set_village_of_birth(self, new):
        self.village_of_birth = new

    def get_village_of_birth(self):
        return self.village_of_birth

    def show_village_of_birth(self):
        print(self.village_of_birth)
    #  ============village_of_birth===============================

    def set_town_of_birth(self, new):
        self.town_of_birth = new

    def get_town_of_birth(self):
        return self.town_of_birth

    def show_town_of_birth(self):
        print(self.town_of_birth)
    #  ============town_of_birth===============================

    def set_year_of_birth(self, new):
        self.year_of_birth = new

    def get_year_of_birth(self):
        return self.year_of_birth

    def show_year_of_birth(self):
        print(self.year_of_birth)
    #  ============year_of_birth===============================

    def set_day_of_birth(self, new):
        self.day_of_birth = new

    def get_day_of_birth(self):
        return self.day_of_birth

    def show_day_of_birth(self):
        print(self.date_of_birth)
    #  ============day_of_birth===============================

    def set_month_of_birth(self, new):
        self.month_of_birth = new

    def get_month_of_birth(self):
        return self.month_of_birth

    def show_month_of_birth(self):
        print(self.month_of_birth)
    #  ============month_of_birth===============================

    def set_continent_of_birth(self, new):
        self.continent_of_birth = new

    def get_continent_of_birth(self):
        return self.continent_of_birth

    def show_continent_of_birth(self):
        print(self.continent_of_birth)
    #  ============continent_of_birth===============================

    def set_mother_tongue(self, new):
        self.mother_tongue = new

    def get_mother_tongue(self):
        return self.mother_tongue

    def show_mother_tongue(self):
        print(self.mother_tongue)
    #  ============mother_tongue===============================

    def set_is_polyglot(self, new):
        self.is_polyglot = new

    def get_is_polyglot(self):
        return self.is_polyglot

    def show_is_polyglot(self):
        print(self.is_polyglot)
    #  ============is_polyglot===============================

    def set_country_of_residence(self, new):
        self.country_of_residence = new

    def get_country_of_residence(self):
        return self.country_of_residence

    def show_country_of_residence(self):
        print(self.country_of_residence)
    #  ============country_of_residence===============================

    def set_state_of_residence(self, new):
        self.state_of_residence = new

    def get_state_of_residence(self):
        return self.state_of_residence

    def show_state_of_residence(self):
        print(self.state_of_residence)
    #  ============state_of_residence===============================

    def set_address_of_residence(self, new):
        self.address_of_residence = new

    def get_address_of_residence(self):
        return self.address_of_residence

    def show_address_of_residence(self):
        print(self.address_of_residence)
    #  ============address_of_residence===============================

    def set_permit_type(self, new):
        self.permit_type = new

    def get_permit_type(self):
        return self.permit_type

    def show_permit_type(self):
        print(self.permit_type)
    #  ============permit_type===============================

    def set_is_resident(self, new):
        self.is_resident = new

    def get_is_resident(self):
        return self.is_resident

    def show_is_resident(self):
        print(self.is_resident)
    #  ============is_resident===============================

    def set_is_citizen(self, new):
        self.is_citizen = new

    def get_is_citizen(self):
        return self.is_citizen

    def show_is_citizen(self):
        print(self.is_citizen)
    #  ============is_citizen===============================

    def set_street_of_residence(self, new):
        self.street_of_residence = new

    def get_street_of_residence(self):
        return self.street_of_residence

    def show_street_of_residence(self):
        print(self.street_of_residence)
    #  ============street_of_residence===============================

#
#


































