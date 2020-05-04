class Vector(object):
    def __init__(self):
        self._elements = []
        self._interation = 0

    def __setitem__(self, index, data):
        self._elements[index] = data

    def __iter__(self):
        self._interation = 0
        return self

    def __getitem__(self, index):
        return self._elements[index]

    def __next__(self):
        try:
            rez = self._elements[self._interation]
            self._interation += 1
            return rez
        except IndexError:
            raise StopIteration

    def __len__(self):
        return len(self._elements)

    def __delitem__(self, index):
        del self._elements[index]

    def __str__(self):
        return  '[{}]'.format(",".join(str(i) for i in self._elements))

    def load_list(self, lst):
        self._elements = lst[:]

def Filter(list, check):
    lst = []
    for item in list:
        if check(item) is True:
            lst.append(item)
    return lst

def MySort(list, check):
    i = 0
    while(i < len(list)):
        if i == 0:
            i = i + 1
        elif check(list[i - 1], list[i]) is True:
            i += 1
        else:
            list[i - 1], list[i] = list[i], list[i - 1]
            i -= 1
    return list