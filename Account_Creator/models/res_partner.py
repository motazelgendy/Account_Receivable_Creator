# -*- coding: utf-8 -*-

from odoo import models, fields, api


class account_creator(models.Model):
    _inherit = 'res.partner'



    def _compute_account_code(self,account_type):
       chart_code = self.env['account.account'].search([('account_type','=',account_type)])
       accoutcodes = []
       for id in chart_code:
            accoutcodes.append(id.code)

       account_code = max([eval(code) for code in accoutcodes]) + 1
       for code in accoutcodes:
         if str(account_code) == code :
            arr = list(str(account_code))
            for i in range(3):
                arr.insert(2,'0')
            account_code = ''.join(arr)
         
       return str(account_code)
            
                


    @api.model
    def create(self, vals):
        
        try: 
         if vals['supplier_rank'] > 0:
               
               account_id = self.env['account.account'].create(
                   {'code':self._compute_account_code('liability_current'),'name':vals['name'],'account_type': 'liability_payable'})
               vals['property_account_payable_id'] = account_id
        except:
                
                account_id = self.env['account.account'].create({'code':self._compute_account_code('asset_current'),'name':vals['name'],'account_type': 'asset_receivable'})
                vals['property_account_receivable_id'] = account_id

        partner_id = super().create(vals)
        return partner_id




        