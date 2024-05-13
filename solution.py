import math


class Date:
    __months = {'01': ('янв', 31),
                '02': ('фев', 28),
                '03': ('мар', 31),
                '04': ('апр', 30),
                '05': ('май', 31),
                '06': ('июн', 30),
                '06': ('июн', 31),
                '07': ('июл', 31),
                '08': ('авг', 31),
                '09': ('сен', 30),
                '10': ('окт', 31),
                '11': ('ноя', 30),
                '12': ('дек', 31)
                }

    def __init__(self, date: str):
        self.__date = date
        if not self.legal():
            print('ошибка')
            self.__date = None

    def legal(self):
        if not isinstance(self.__date, str):
            return False

        if self.__date.count('.') != 2 or not self.__date.replace('.', '').isdigit():
            return False
        day, month, year = self.__date.split('.')

        if len(month) != 2 or len(day) != 2 or len(year) != 4:
            return False

        if month not in self.__months.keys():
            return False

        if int(day) > 29 and int(year) % 4 == 0 and month == '02':
            return False

        if int(day) > self.__months[month][1] and not (int(year) % 4 == 0 and month == '02'):
            return False

        return True

    @property
    def day(self):
        if not self.legal():
            return None
        return self.__date.split('.')[0]

    @property
    def month(self):
        if not self.legal():
            return None
        return self.__date.split('.')[1]

    @property
    def year(self):
        if not self.legal():
            return None
        return self.__date.split('.')[2]

    @property
    def date(self):
        if not self.legal():
            return None
        return f'{int(self.day)} {self.__months[self.month][0]} {self.year} г.'

    @date.setter
    def date(self, new):
        self.__date = new
        if not self.legal():
            print('ошибка')
            self.__date = None

    def to_timestamp(self):
        if not self.legal():
            return False
        return sum([(365 + (year % 4 == 0)) * 86400 for year in range(1970, int(self.year))]) + \
            (sum([days[1] + (int(self.year) % 4 == 0 and month == '02') for month, days in self.__months.items()
                  if int(month) < int(self.month)]) + int(self.day) - 1) * 86400

    def __repr__(self):
        return str(self.date)

    def __lt__(self, other):
        return self.to_timestamp() < other.to_timestamp()

    def __le__(self, other):
        return self.to_timestamp() <= other.to_timestamp()

    def __eq__(self, other):
        return self.to_timestamp() == other.to_timestamp()

    def __ne__(self, other):
        return self.to_timestamp() != other.to_timestamp()

    def __gt__(self, other):
        return self.to_timestamp() > other.to_timestamp()

    def __ge__(self, other):
        return self.to_timestamp() >= other.to_timestamp()


class AirTicket:
    def __init__(self, passenger_name: str, _from, to, date_time, flight, seat, _class, gate):
        self.passenger_name = passenger_name
        self._from = _from
        self.to = to
        self.date_time = date_time
        self.flight = flight
        self.seat = seat
        self._class = _class
        self.gate = gate

    def __repr__(self):
        return f'|{self.passenger_name.ljust(16)}' \
               f'|{self._from.ljust(4)}' \
               f'|{self.to.ljust(3)}' \
               f'|{self.date_time.ljust(16)}' \
               f'|{self.flight.ljust(20)}' \
               f'|{self.seat.ljust(4)}' \
               f'|{self._class.ljust(3)}' \
               f'|{self.gate.ljust(4)}|'


class Load:
    data = []

    @classmethod
    def write(cls, *args):
        for f in args:
            with open(f, encoding='utf8') as file:
                lines = file.readlines()
            if 'passenger_name' in lines[0]:
                for line in lines[1:]:
                    info = line.replace('\n', '')[:-1].split(';')
                    Load.data.append(AirTicket(*info))
            elif 'id;nick_name;first_name;last_name;middle_name;gender;' in lines[0]:
                for line in lines[1:]:
                    info = line.replace('\n', '')[:-1].split(';')
                    Meeting.persons[info[0]] = User(*info)
            elif 'id;date;title;' in lines[0]:
                for line in lines[1:]:
                    info = line.replace('\n', '')[:-1].split(';')
                    Meeting(*info)
            elif 'id_meet;id_pers;' in lines[0]:
                for line in lines[1:]:
                    info = line.replace('\n', '')[:-1].split(';')
                    if Meeting.pers_meetings.get(info[0]):
                        Meeting.pers_meetings[info[0]].append(info[1])
                    else:
                        Meeting.pers_meetings[info[0]] = [info[1]]

        for meet in Meeting.lst_meeting:
            for pers_id in Meeting.pers_meetings[meet.id]:
                meet.add_person(Meeting.persons[pers_id])


class Meeting:
    lst_meeting = []
    persons = {}
    pers_meetings = {}

    def __init__(self, id, date, title):
        self.id = id
        self.date = Date(date)
        self.title = title
        self.__employees = []
        Meeting.lst_meeting.append(self)

    def __repr__(self):
        info = f'Рабочая встреча {self.id}\n' \
               f'{self.date} {self.title}\n'

        for employee in self.__employees:
            info += f'{employee}\n'

        return info

    def add_person(self, person):
        self.__employees.append(person)

    def count(self):
        return len(self.__employees)

    @classmethod
    def count_meeting(cls, date):
        return len([meeting for meeting in Meeting.lst_meeting if meeting.date == date])

    @classmethod
    def total(cls):
        return sum([meeting.count() for meeting in Meeting.lst_meeting])


class User:
    def __init__(self, id, login, first_name, last_name, middle_name, gender):
        self.id, self.login, self.first_name, self.last_name, self.middle_name, self.gender = \
            id, login, first_name, last_name, middle_name, gender

    def __repr__(self):
        info = f'ID: {self.id} LOGIN: {self.login} NAME: '

        if self.first_name:
            info += f'{self.first_name} '
        if self.last_name:
            info += f'{self.last_name} '
        if self.middle_name:
            info += f'{self.middle_name} '
        if self.gender:
            info += f'GENDER: {self.gender} '

        return info


class GeometricObject:
    def __init__(self, x=0.0, y=0.0, color='black', filled=False):
        self.__x, self.__y, self.color, self.filled = x, y, color, filled

    def set_coordinate(self, x, y):
        self.__x, self.__y = float(x), float(y)

    def set_color(self, color):
        self.color = color

    def set_filled(self, filled):
        self.filled = filled

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_color(self):
        return self.color

    def is_filled(self):
        return self.filled

    def __str__(self):
        return f'({float(self.__x)}, {float(self.__y)})\n' \
               f'color: {self.color}\n' \
               f'filled: {self.filled}'

    def __repr__(self):
        return f'({int(self.__x)}, {int(self.__y)}) {self.color} ' \
               f'{"filled" if self.filled else "not filled"}'


class Circle(GeometricObject):
    def __init__(self, x=0.0, y=0.0, radius=0.0, color='black', filled=False):
        super().__init__(x, y, color, filled)
        self.__radius = max(float(radius), 0.0)

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, new):
        self.__radius = max(float(new), 0.0)

    def get_area(self):
        return math.pi * self.__radius**2

    def get_perimetr(self):
        return 2 * math.pi * self.__radius

    def get_diametr(self):
        return 2 * self.__radius

    def __str__(self):
        return f'radius: {self.radius}\n' \
               f'{super().__str__()}'

    def __repr__(self):
        return f'radius: {int(self.radius)} ' \
               f'{super().__repr__()}'


class Rectangle(GeometricObject):
    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0, color='black', filled=False):
        super().__init__(x, y, color, filled)
        self.width, self.height = max(float(width), 0.0), max(float(height), 0.0)

    def set_width(self, new):
        self.width = max(float(new), 0.0)

    def set_height(self, new):
        self.height = max(float(new), 0.0)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_area(self):
        return self.width * self.height

    def get_perimetr(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return f'width: {self.width}\n' \
               f'height: {self.height}\n' \
               f'{super().__str__()}'

    def __repr__(self):
        return f'width: {int(self.width)} ' \
               f'height: {int(self.height)} ' \
               f'{super().__repr__()}'
