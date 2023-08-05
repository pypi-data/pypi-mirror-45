# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .category import *
from .party import *
from .address import *
from .contact_mechanism import *
from .configuration import *


def register():
    Pool.register(
        Category,
        Party,
        PartyLang,
        PartyCategory,
        PartyIdentifier,
        CheckVIESResult,
        PartyReplaceAsk,
        Address,
        AddressFormat,
        ContactMechanism,
        Configuration,
        ConfigurationSequence,
        ConfigurationLang,
        module='party', type_='model')
    Pool.register(
        CheckVIES,
        PartyReplace,
        module='party', type_='wizard')
