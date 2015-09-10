# -*- coding: utf-8 -*-
'''
lucterios.contacts package

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2015 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lucterios.framework.tools import FORMTYPE_MODAL, MenuManage, CLOSE_NO
from lucterios.framework.xfergraphic import XferContainerCustom,\
    XferContainerAcknowledge
from lucterios.framework.xfercomponents import XferCompButton, XferCompImage,\
    XferCompLabelForm
from lucterios.CORE.parameters import Params
from lucterios.CORE.views import ParamEdit
from lucterios.framework.error import LucteriosException, IMPORTANT
from lucterios.mailing.functions import will_mail_send, send_email


@MenuManage.describ('CORE.change_parameter', FORMTYPE_MODAL, 'contact.conf', _('Change mailing parameters'))
class Configuration(XferContainerCustom):
    icon = "config_mail.png"
    caption = _("Mailing parameters")

    def fillresponse(self):
        XferContainerCustom.fillresponse(self)
        img = XferCompImage('img')
        img.set_value(self.icon_path())
        img.set_location(0, 0, 1, 6)
        self.add_component(img)
        lbl = XferCompLabelForm('title')
        lbl.set_value_as_title(_('EMail configuration'))
        lbl.set_location(1, 0, 2)
        self.add_component(lbl)

        conf_params = ['mailing-smtpserver', 'mailing-smtpport',
                       'mailing-smtpsecurity', 'mailing-smtpuser', 'mailing-smtppass']
        Params.fill(self, conf_params, 1, 1)
        btn = XferCompButton('editparam')
        btn.set_location(3, 1, 1, 5)
        btn.set_action(self.request, ParamEdit.get_action(
            _('Modify'), 'images/edit.png'), {'close': CLOSE_NO, 'params': {'params': conf_params}})
        self.add_component(btn)
        if will_mail_send():
            btn = XferCompButton('tryemail')
            btn.set_location(1, 10, 2)
            btn.set_action(self.request, SendEmailTry.get_action(
                _('Send'), ''), {'close': CLOSE_NO})
            self.add_component(btn)


@MenuManage.describ('CORE.change_parameter')
class SendEmailTry(XferContainerAcknowledge):
    icon = "config_mail.png"
    caption = _("EMail try")

    def fillresponse(self):
        if not will_mail_send():
            raise LucteriosException(IMPORTANT, _('Bad email parameter!'))
        send_email(
            None, _("EMail try"), _('EMail sent to check configuration'))
        self.message(_("EMail send, check it."))