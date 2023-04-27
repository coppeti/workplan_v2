from dataclasses import dataclass
from typing import ClassVar
from datetime import date, timedelta, datetime
import calendar

@dataclass
class Holidays:
    """Holidays must be used to get a dicts list of holidays for differents cantons in Switzerland.
    You can also get individual holiday date as Easter, Pentecost etc.
    To build your instance you can pass 3 arguments:
        year, region, language.

    Attributes:
        year (int): Year of your holidays list, four digits (Optional, default: current year)
        region (str): Region of your holidays list, two lowercase letters. \
            Available value: be, so, ag, fr, ne, vd and ge (Optional, default: be)
        language (srt): Names's language of your holidays list, two lowercase letters. \
            Available values: de or fr (Optional, default: de)

    Methods:
        calc_easter(self)
            Return Easter date

            Args:
                No argument

        calc_goodfriday(self)
            Return Goodfriday date

            Args:
                No argument

        calc_eastermonday(self)
            Return Eastermonday date

            Args:
                No argument

        calc_ascension(self)
            Return Ascension date

            Args:
                No argument

        calc_pentecost(self)
            Return Pentecost date

            Args:
                No argument

        calc_whitmonday(self)
            Return Whitmonday date

            Args:
                No argument

        calc_vdfastday(self)
            Return Fastday date of Vaud

            Args:
                No argument

        calc_gefastday(self)
            Return Fastday date of Geneva

            Args:
                No argument

        calc_corpuschristi(self)
            Return Corpus Christi date

            Args:
                No argument

        all_dates(self)
            Return the list of all holidays in Switzerland for a given year

            Args:
                No argument

        hdays(self)
            Main method. Will return the list of holidays for a given year, given region and given language

            Args:
                No argument

        other_hdays(self)
            Return all holidays there are not in Bern canton. Used to color the annual calendar

            Args:
                no argument
    """
    de_names: ClassVar[list] = ['Neujahr',  # 0
                                'Bercht<wbr>olds<wbr>tag',  # 1
                                'Tag der Republik NE',  # 2
                                'Josefstag',  # 3
                                'Kar<wbr>frei<wbr>tag',  # 4
                                'Ostern',  # 5
                                'Oster<wbr>mon<wbr>tag',  # 6
                                'Arbeits<wbr>tag',  # 7
                                'Auffahrt',  # 8
                                'Pfing<wbr>sten',  # 9
                                'Pfingst<wbr>mon<wbr>tag',  # 10
                                'Fron<wbr>leich<wbr>nam',  # 11
                                'National<wbr>feier<wbr>tag',  # 12
                                'Mariä Him<wbr>mel<wbr>fahrt',  # 13
                                'Genfer Bet<wbr>tag',  # 14
                                'Bettags<wbr>mon<wbr>tag',  # 15
                                'Aller<wbr>hei<wbr>ligen',  # 16
                                'Mariä Emp<wbr>fäng<wbr>nis',  # 17
                                'Weih<wbr>nach<wbr>ten',  # 18
                                'Stephans<wbr>tag', # 19
                                'Wieder<wbr>herstel<wbr>lung GE']  # 20
    fr_names: ClassVar[list] = ['Nouvel An',  # 0
                                'Berchtold',  # 1
                                'Jour de la Répu<wbr>blique NE',  # 2
                                'Saint Joseph',  # 3
                                'Vendredi Saint',  # 4
                                'Pâques',  # 5
                                'Lundi de Pâques',  # 6
                                'Jour du Travail',  # 7
                                'Ascension',  # 8
                                'Pentecôte',  # 9
                                'Lundi de Pente<wbr>côte',  # 10
                                'Fête Dieu',  # 11
                                'Fête Natio<wbr>nale',  # 12
                                'Assomption',  # 13
                                'Jeûne gene<wbr>vois',  # 14
                                'Lundi du Jeûne',  #15
                                'Toussaint',  # 16
                                'Immaculée Con<wbr>cep<wbr>tion',  # 17
                                'Noël',  # 18
                                'Saint Etienne',  # 19
                                'Restaura<wbr>tion GE']  # 20
    # ne_indexes is declared in self named method
    ag_indexes: ClassVar[list] = [0, 1, 4, 5, 6, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19]
    be_indexes: ClassVar[list] = [0, 1, 4, 5, 6, 8, 9, 10, 12, 18, 19]
    bs_indexes: ClassVar[list] = [0, 4, 5, 6, 7, 8, 9, 10, 12, 18, 19]
    fr_indexes: ClassVar[list] = [0, 1, 4, 5, 6, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19]
    ge_indexes: ClassVar[list] = [0, 3, 4, 5, 6, 8, 9, 10, 12, 14, 18, 20]
    so_indexes: ClassVar[list] = [0, 1, 4, 5, 8, 9, 11, 12, 13, 16, 18]
    vd_indexes: ClassVar[list] = [0, 1, 4, 5, 6, 8, 9, 10, 12, 15, 18]
    vs_indexes: ClassVar[list] = [0, 1, 3, 5, 6, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19]

    year: int = datetime.today().year
    region: str = 'be'
    language: str = 'de'

    # Get NE indexes. If 1.01 or 25.12 are Sunday, next day is holiday.
    def ne_indexes(self):
        base = [0, 2, 4, 5, 7, 8, 9, 12, 18]
        if date(self.year, 1, 1).weekday() == 6:
            base.append(1)
        if date(self.year, 12, 25).weekday() == 6:
            base.append(19)
        return sorted(base)

    # Get Easter date (Sunday) for a given year
    def calc_easter(self):
        y=self.year//100
        b=self.year%100
        c=(3*(y+25))//4
        d=(3*(y+25))%4
        e=(8*(y+11))//25
        f=(5*y+b)%19
        g=(19*f+c-e)%30
        h=(f+11*g)//319
        j=(60*(5-d)+b)//4
        k=(60*(5-d)+b)%4
        m=(2*j-k-g+h)%7
        n=(g-h+m+114)//31
        p=(g-h+m+114)%31
        day=p+1
        month=n
        return date(self.year, month, day)

    # Get Goodfriday date for a given year
    def calc_goodfriday(self):
        return self.calc_easter() + timedelta(days=-2)

    # Get Eastermonday date for a given year
    def calc_eastermonday(self):
        return self.calc_easter() + timedelta(days=1)

    # Get Ascension date for a given year
    def calc_ascension(self):
        return self.calc_easter() + timedelta(days=39)

    # Get Pentecost date for a given year
    def calc_pentecost(self):
        return self.calc_easter() + timedelta(days=49)

    # Get Whitmonday for a given year
    def calc_whitmonday(self):
        return self.calc_easter() + timedelta(days=50)

    # Get Vaud Fastday date for a given year
    def calc_vdfastday(self):
        c = calendar.Calendar()
        return date(self.year, 9, (c.monthdayscalendar(self.year, 9)[2][6])) + timedelta(days=1)

    # Get Geneva Fastday date for a given year
    def calc_gefastday(self):
        c = calendar.Calendar()
        return date(self.year, 9, (c.monthdayscalendar(self.year, 9)[0][6])) + timedelta(days=4)

    # Get Corpus Christi date for a given year
    def calc_corpuschristi(self):
        return self.calc_easter() + timedelta(days=60)

    # All CH holidays for a given year
    def all_dates(self):
        return [date(self.year, 1, 1),  #0
                date(self.year, 1, 2),  #1
                date(self.year, 3, 1),  #2
                date(self.year, 3, 19),  #3
                self.calc_goodfriday(),  #4
                self.calc_easter(),  #5
                self.calc_eastermonday(),  #6
                date(self.year, 5, 1),  #7
                self.calc_ascension(),  #8
                self.calc_pentecost(),  #9
                self.calc_whitmonday(),  #10
                self.calc_corpuschristi(),  #11
                date(self.year, 8, 1),  #12
                date(self.year, 8, 15),  #13
                self.calc_gefastday(),  #14
                self.calc_vdfastday(),  #15
                date(self.year, 11, 1),  #16
                date(self.year, 12, 8),  #17
                date(self.year, 12, 25),  #18
                date(self.year, 12, 26),  #19
                date(self.year, 12, 31)]  #20


    def hdays(self):
        hdays = []
        # Region
        if self.region == 'so':
            indexes = Holidays.so_indexes
        elif self.region == 'ag':
            indexes = Holidays.ag_indexes
        elif self.region == 'fr':
            indexes = Holidays.fr_indexes
        elif self.region == 'ne':
            indexes = self.ne_indexes()
        elif self.region == 'vd':
            indexes = Holidays.vd_indexes
        elif self.region == 'ge':
            indexes = Holidays.ge_indexes
        elif self.region == 'bs-bl':
            indexes = Holidays.bs_indexes
        elif self.region == 'vs':
            indexes = Holidays.vs_indexes
        else:
            indexes = Holidays.be_indexes
        # Language
        if self.language == 'fr':
            names = Holidays.fr_names
        else:
            names = Holidays.de_names
        # Holidays dates result
        hdays = {date:names[self.all_dates().index(date)] for date in self.all_dates() if self.all_dates().index(date) in indexes}
        return hdays


    def other_hdays(self):
        other_hdays = {date:Holidays.de_names[self.all_dates().index(date)]
                       for date in self.all_dates() if self.all_dates().index(date) not in Holidays.be_indexes}
        return other_hdays