# Django-Searchly-Tables

A simple Django app that adds search and sort to HTML tables.

I like using simple views, but it should work with class-based views as well (but I haven't tested it).

## Example

Add `searchly_tables` to your `INSTALLED_APPS`:

	INSTALLED_APPS = (
		...,
		"searchly_tables",
	)

In your view.py, import searchly_tables, add a new table to a view,
and specify for which model you would like to use it:

	from django.shortcuts import render

	from example.model import ExampleModel
	from searchly_tables.tables import SearchlyTable

	def view(request):
		table = SearchlyTable(module="exampleapp.models", model="ExampleModel", field_filters=field_filters)
		table.labels = {'baseField1': 'labelForBaseField1', 'foreignkey_relationship': 'labelForForeignKeyRelationship', 'baseField2': 'labelForBaseField2'}

		# Optional links to models in fields
		table.field_links = {'baseField2': ['app:view': 'url_parameter']}
		if request.POST:
			table.post(request.POST, filter=True, sort=True)
		return render(request, 'example/table.html', {'table': table})

Then add the table to your template like this:

	<form action="#" method=POST>
		{% csrf_token %}
		{{ table.searchbar|safe }}
		<table>
			{{ table.header|safe }} {{ table.body|safe }}
		</table>
	</form>

And that's it! Naturally, you can change the appearance of the table by applying CSS.

For instance `table.attrs['td'] = 'my_td_class'` would result in `<td class="my_td_class">` on all td elements in the table.
Django-searchly-tables currently only supports classes; sorry, no direct styles as of yet.
Also no direct access to a single element by id for most elements; the sole exception is `<td>`.

Here's the list of elements I use in the table:

> _thead_, _tbody_, _tr_, _th_, _td_, _input_, _button_, _select_, _option_

## FAQ

_Should I use this?_

Maybe? Probably not?

It's a super basic app with very little fuzz. The code is still all over the place.
If that's for you, cool. If you need more options in your tabling(?),
you should check out [django_tables2](https://django-tables2.readthedocs.io).

_Another table app? Haven't you heard about django\_tables2? It's way better and has tons of features!_

Yep, I agree. I even linked to it in my earlier answer!

_So, will this support feature X in the future? I really need that._

Probably not? I'm happy with the way it works now, apart from some minor issues (=code cleanup/documentation).
But you're welcome to fork it, if you need feature X. Or use django_tables2 (seriously, it's great!).
