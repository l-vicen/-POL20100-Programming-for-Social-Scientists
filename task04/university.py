from __future__ import annotations

import copy


class Person:
    def __init__(self, name: str, age: int):
        if age <= 0:
            raise ValueError()
        self.name = name
        self.age = age

    def __lt__(self, other):
        return self.age < other.age

    def __repr__(self):
        return f'Person(name="{self.name}", age={self.age})'

    def __str__(self):
        return f'{self.name}'


class Student(Person):
    def __init__(self, identifier: str, name: str, age: int, semester: int = 1):
        super().__init__(name, age)
        self.identifier = identifier
        if semester < 1:
            raise ValueError()
        else:
            self.semester = semester

    def __repr__(self):
        return f'Student(identifier="{self.identifier}", name="{self.name}", age={self.age}, semester={self.semester})'

    def __str__(self):
        return f'{self.name}'

    def __eq__(self, other):
        return True if self.identifier == other.identifier else False


class Professor(Person):
    def __init__(self, name: str, age: int, room: str):
        super().__init__(name, age)
        self.room = room

    def __repr__(self):
        return f'Professor(name="{self.name}", age={self.age}, room="{self.room}")'

    def __str__(self):
        return f'{"Prof. " + self.name}'


class Lecture:
    def __init__(
            self,
            title: str,
            lecturer: Professor,
            participants: list[Student] = [],
            prerequisites: list[Lecture] = [],
    ):
        self.title = title
        self.lecturer = lecturer
        self.preStorage = set()
        self.iterations = 0
        self.count = 0

        if (len(participants) != 0):
            self.participants = participants
        else:
            self.participants = []

        if (len(prerequisites) != 0):
            self.prerequisites = set(prerequisites)
        else:
            self.prerequisites = set()

    def __len__(self) -> int:
        return len(self.participants)

    def __repr__(self):
        return f'Lecture(title="{self.title}", lecturer={repr(self.lecturer)}, participants={self.participants}, prerequisites={self.prerequisites})'

    @property
    def all_prerequisites(self) -> set[Lecture]:
        if len(self.prerequisites) == 0:
            return self.preStorage
        else:
            it = len(self.prerequisites)
            tmpStorage = []
            for i in range(it):
                print(f'Iteration {i}')
                for lecture in self.prerequisites:
                    print(f'Lecture {lecture}')
                    tmpStorage.append(lecture)
                    self.all_prerequisites(lecture)



        # if len(self.prerequisites) == 0:
        #     return self.preStorage
        # else:
        #     for lecture in self.prerequisites:
        #         print(f'Considering {lecture}')
        #         self.preStorage.add(lecture)
        #         if (len(lecture.prerequisites) == 0):
        #             continue
        #         if (len(lecture.prerequisites) == 1):
        #             for lectureDep in lecture.prerequisites:
        #                 if lectureDep not in self.preStorage:
        #                     self.preStorage.add(lectureDep)
        #
        #     return self.preStorage


if __name__ == "__main__":
    platon = Professor(name="Platon", age=42, room="42")
    platon = Professor(name="Platon", age=42, room="42")
    lecture1 = Lecture(title="A", lecturer=platon)
    print(lecture1.prerequisites)
    lecture2 = Lecture(title="B", lecturer=platon, prerequisites=[lecture1])
    print('**********************************')
    print(lecture2.all_prerequisites)

    # print({lecture1, lecture2})
    # print('**********************************')
    # print(lecture3.all_prerequisites)


