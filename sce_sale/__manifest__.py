# -*- coding: utf-8 -*-
{
    'name': "sce_sale",

    'summary': """
        SCENERGY SALE""",

    'description': """
        SCENERGY SALE
    """,

    'author': "Karizma Conseil",
    'website': "http://www.karizma-conseil.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale_management',
        'sale',
        'web_domain_field',
        'report_qweb_element_page_visibility',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/sale_order_views.xml',
        'views/product_views.xml',
        'views/distribution_network_group.xml',
        'report/layout_report.xml',
        'report/sce_sale_report_pv.xml',
        'report/sce_sale_report_pac.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'sce_sale/static/src/css/sale_custom_scss.scss',
    #     ]
    # }


}
