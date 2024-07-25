# -*- coding: utf-8 -*-

from odoo import models, fields, api


class account__creator_esnad(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        chart_code = self.env['account.account'].search([('account_type','=','asset_current')])
        accoutcodes = []
        for id in chart_code:
            accoutcodes.append(id.code)

        account_code = max([eval(i) for i in accoutcodes]) + 1
        

        for i in chart_code:
         if str(account_code) == i.code :
            arr = list(str(account_code))
            for i in range(3):
                arr.insert(2,'0')
            
            account_code = ''.join(arr)
        

        account_receivable_data = {
            'code': str(account_code),
            'name': vals['name'],
            'account_type': 'asset_receivable'

        }

        account_receivable_id = self.env['account.account'].create(account_receivable_data)
        vals['property_account_receivable_id'] = account_receivable_id
        partner_id = super().create(vals)
        return partner_id