# -*- coding: utf-8 -*-


class WrongQueryGiven(Exception):
    pass


class NoContentFound(Exception):
    pass


class NoFilterGiven(Exception):
    pass


class WrongSpecialGiven(Exception):
    pass


class NoOrderByAttributeGiven(Exception):
    pass


class TooMuchOrderByAttributesGiven(Exception):
    pass


class WrongOrderByAttribute(Exception):
    pass


class FieldNotFoundException(Exception):
    pass


class WrongInstanceToSave(Exception):
    pass


class WrongInstanceToDrop(Exception):
    pass
