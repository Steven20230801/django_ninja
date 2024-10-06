# yourapp/templatetags/form_tags.py
from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_class):
    """
    自定义模板过滤器，用于向表单字段添加 CSS 类。
    使用方法：{{ form.field_name|add_class:"css-class-name" }}
    """
    return field.as_widget(attrs={"class": css_class})
