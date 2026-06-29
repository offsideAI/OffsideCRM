from crudbuilder.abstract import BaseCrudBuilder
from .models import Product

class ProductCrud(BaseCrudBuilder):
    model = Product
    search_fields = ['name']
    tables2_fields = ('cat', 'name', 'slug', 'description', 'created_user', 'price', 'image', 'thumbnail')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 20  # default is 10
    modelform_excludes = ['created_at']