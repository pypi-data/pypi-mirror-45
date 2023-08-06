# coding: utf-8

import importlib
import datetime

from django.contrib.admin.utils import get_fields_from_path, label_for_field
from django.urls import reverse
from django.core.exceptions import FieldDoesNotExist
from django.utils import timezone

def _strToClass(moduleName, className):
	module = importlib.import_module(moduleName)
	return getattr(module, className)

class SearchlyTable(object):
	''' Class that takes a Django model and spits out a sortable HTML table.'''
	DEFAULT_ATTRS = {'thead': '', 'tbody': '', 'input': '', 'button': '', 'select': '', 'option': '', 'tr': '', 'th': '', 'td': ''}
	attrs = DEFAULT_ATTRS
	fields = {}
	date_format = '%d.%B %Y %H:%M'

	def __init__(self, module, model, filter_query="", field_filters = {}, subset=None, subset_size=25, use_verbose=True):
		self.model = model
		self.module = module
		self.filter_query = filter_query
		self.field_filters = field_filters
		self.queryset = _strToClass(self.module, self.model).objects.all()
		if use_verbose == True:
			self.verbose_fields = [f.verbose_name for f in _strToClass(self.module, self.model).objects.first()._meta.fields]
		fields = _strToClass(self.module, self.model)._meta.get_fields()
		self.labels = {}
		for field in fields:
			self.labels["{}".format(field.name)] = field
		if self.filter_query != "":
			_fi = self.filter_query.split('=')
			if _fi[0] in self.field_filters:
				attribute = "{}".format(self.field_filters[_fi[0]])
			else:
				attribute = "{}__{}".format(_fi[0], "icontains")
			self.queryset = self.queryset.filter(**{attribute: _fi[1]})
		if subset == None:
			self.subset = self.queryset
		self.subset_size = subset_size

	@property
	def queryset(self):
		return self._queryset

	@queryset.setter
	def queryset(self, value):
		self._queryset = value

	def sort(self, data):
		if "up" in data:
			self._sort(data['up'])
		elif "down" in data:
			self._sort(data['down'], True)

	def _sort(self, attribute, reverse=False):
		if reverse:
			attribute = "-{}".format(attribute)
		self.queryset = self.queryset.order_by(attribute)

	def filter(self, data):
		if 'search_query' in data and 'reset' not in data:
			if data['search_query'] != '':
				attr = data['header_attribute']
				query = data['search_query']
				self._filter(attr, query)
				self.filter_query = "{}={}".format(attr, query)
		elif 'reset' in data:
			self.queryset = _strToClass(self.module, self.model).objects.all()
			self.filter_query = ""

	def _filter(self, attribute, value, modifier="icontains"):
		if attribute in self.field_filters:
			attribute = "{}".format(self.field_filters[attribute])
		else:
			attribute = "{}__{}".format(attribute, modifier)
		self.queryset = self.queryset.filter(**{attribute: value})

	def searchbar(self):
		filter_query = '<input type=hidden name=filter_query value="{}"></input>'.format(self.filter_query)
		selector = '<select name=header_attribute>'
		for key, value in self.labels.items():
			selector += '<option value="{}">{}</option>'.format(key, value)
		selector += '</select>'
		reset = '<button name=reset class="{}">Reset</button>'.format(self.attrs['button'])
		_str = '{}{}<input type=text name=search_query class="{}"><button>Go</button></input>{}' \
			.format(filter_query, selector, self.attrs['input'], reset)
		return _str

	def header(self):
		_str = '<thead class="{}"><tr class="{}">'.format(self.attrs['thead'], self.attrs['tr'])
		className = _strToClass(self.module, self.model)
		for key, value in self.labels.items():
			if key == '_selector':
				_str += '<th class="{}">{}</th>'.format(self.attrs['th'], value)
			else:
				_str += '<th class="{}">{}<button name=up value={}>↑</button><button name=down value={}>↓</button></th>' \
					.format(self.attrs['th'], value, key, key, key)
		_str += '</tr></thead>'
		return _str

	def body(self):
		_str = '<tbody class="{}">'.format(self.attrs['tbody'])
		className = _strToClass(self.module, self.model)
		queryset = self.subset
		for obj in queryset:
			_str += '<tr class="{}">'.format(self.attrs['tr'])
			for field in self.labels.keys():
				if field == '_selector':
					_str += '<td class="{}" id="{}"><input type="checkbox" name="checkbox" value="{}" /></td>' \
						.format(self.attrs['td'], field, obj.pk)
				elif '__' in field:
					if field in self.field_links.keys():
						fields = field.split('__')
						field_list = self.field_links[field]
						field_link_value = "__".join(fields[:-1]) + "__{}".format(self.field_links[field][1])
						display_link = self.queryset.filter(pk=obj.pk).values_list(*[field_link_value]).first()[0].__str__()
						display_field = self.queryset.filter(pk=obj.pk).values_list(*[field]).first()[0].__str__()
						field_link = '<a href="{}">{}</a>' \
							.format(reverse(field_list[0], args=[display_link]), display_field)
						_str += '<td class="{}" id="{}">{}</td>'.format(self.attrs['td'], field, str(field_link))
					else:
						display_field = self.queryset.filter(pk=obj.pk).values_list(*[field]).first()[0].__str__()
						_str += '<td class="{}" id="{}">{}</td>'.format(self.attrs['td'], field, str(display_field))
				elif hasattr(className, field):
					display_field = getattr(obj, field)
					if type(display_field) == list:
						_str += '<td class="{}" id="{}">'.format(self.attrs['td'], field)
						if field in self.field_links.keys():
							for o in display_field:
								field_list = self.field_links[field]
								_str += '<a href="{}">{}</a>, '.format(reverse(field_list[0], args=[o.pk]), o)
						else:
							for o in display_field:
								_str += '{}, '.format(o)
						_str += '</td>'
					else:
						try:
							if hasattr(obj._meta.get_field(field), 'choices'):
								_val = dict(obj._meta.get_field(field).choices).get(display_field, '') or display_field
								id_val = field
								if display_field is None:
									id_val = "{}_{}".format(field, 'none')
								print(display_field)
								if type(display_field) == datetime.datetime:
									_d = timezone.localtime(display_field)
									_val = _d.strftime(self.date_format)
								_str += '<td class="{}" id="{}">{}</td>'.format(self.attrs['td'], id_val, str(_val))
						except FieldDoesNotExist:
							if type(display_field) == datetime.datetime:
								display_field = display_field.strftime(self.date_format)
							if field in self.field_links.keys():
								field_list = self.field_links[field]
								field_link = '<a href="{}">{}</a>' \
									.format(reverse(field_list[0], args=[getattr(obj, v) for v in field_list[1:]]), display_field)
								_str += '<td class="{}" id="{}">{}</td>'.format(self.attrs['td'], field, str(field_link))
							else:
								_str += '<td class="{}" id="{}">{}</td>'.format(self.attrs['td'], field, str(display_field))
			_str += '</tr>'
		_str += '</tbody>'
		return _str

	def post(self, query, filter=False, sort=False):
		if filter:
			self.filter(query)
		if sort:
			self.sort(query)
		if self.subset:
			self.subset = self.queryset[:self.subset_size]