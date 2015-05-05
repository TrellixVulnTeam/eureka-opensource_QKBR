# -*- coding: utf-8 -*-
# =-
# Copyright Solocal Group (2015)
#
# eureka@solocal.com
#
# This software is a computer program whose purpose is to provide a full
# featured participative innovation solution within your organization.
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# =-

from nagare import var, component
from nagare.i18n import _

from eureka.infrastructure import event_management
from eureka.ui.common.menu import Menu


class SearchMenu(Menu):
    """Menu for search widget"""


class SearchBlock(object):
    label = _(u'Search ideas')

    def __init__(self, parent):
        event_management._register_listener(parent, self)
        self.search_pattern = var.Var('')
        self.search_by = var.Var('')

        # Tells if opening animation is already done
        self.form_opened = var.Var(False)

        # Tells if form opening has been asked
        self.show_form = var.Var(False)

        self.options = component.Component(SearchMenu([
            (_(u'search_ideas'), u'idea'),
            (_(u'Profils'), u'profile')]))

        self.options.on_answer(self.select_option)
        self.select_option(u'idea')

    def do_search(self):
        p = self.search_pattern().strip()

        if self.options().selected() == u'idea':
            event_management._emit_signal(self, "SEARCH_IDEAS", pattern=p)
        else:
            event_management._emit_signal(self, "SEARCH_USERS", pattern=p)

    def do_reset(self):
        self.search_pattern = None

    def select_option(self, value):
        self.search_by(value)
        self.options().selected(value)
