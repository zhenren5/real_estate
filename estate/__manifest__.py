{
    "name": "Real Estate",
    "summary": "Real Estate module",
    "version": "18.0.0.0.0",
    "licence": "OEEL-1",
    "depends": ["base","crm"],
    "data":[],
    'application': True,
    "data": [
        # SECURITY
        "security/res_groups.xml", 
        "security/ir.model.access.csv",
        # VIEWS
        "views/real_estate_views.xml",
        "views/estate_type_views.xml",
        "views/estate_tag_views.xml",
        "views/estate_offer_views.xml",
        "views/view_users.xml",
        # MENUS
        "views/estate_menus.xml",
        "views/estate_type_menus.xml",
        "views/estate_tag_menus.xml"
    ],
    "demo": [
        "demo/demo.xml"
    ],
}