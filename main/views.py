import csv
import datetime
import json
import os
import random

from os.path import join
from django.conf import settings
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, HttpResponseRedirect
from .models import Schema, ColumnItem
from django.contrib.auth.decorators import login_required
from faker import Faker


@login_required()
def index(request):
    """Page with list of schemas in DB"""

    schema = Schema.objects.all()

    data = {
        'schema': schema,
    }
    return render(request, 'main/schemas.html', data)


def creating_schema(request):
    """Creating new schema page"""

    return render(request, 'main/new_schema.html')


def save_schema(request):
    """Save schema request. Creating Schema instance"""

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            new_schema = Schema()
            new_schema.name = data['name']
            new_schema.column_separator = data['col_sep']
            new_schema.string_character = data['str_char']
            if new_schema.name != '':
                new_schema.save()
                for col in data['columns']:
                    new_col = ColumnItem()
                    new_col.col_name = col['col_name']
                    new_col.col_type = col['col_type']
                    new_col.order = col['order']
                    new_col.user_id = col['c_id']
                    if col['col_type'] == 'age':
                        new_col.range_min = col['range_min']
                        new_col.range_max = col['range_max']
                    new_col.schema = Schema.objects.get(id=new_schema.id)
                    if new_col.col_name != '' and new_col.order != '':
                        new_col.save()
                return JsonResponse({'status': 200,
                                    'id': f'{new_schema.id}'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def data_req(request, pk):
    """Requesting data for filling fields to edit schema"""

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            obj = Schema.objects.get(id=pk)
            col_list = []
            col = list(ColumnItem.objects.filter(schema=pk).values())

            return JsonResponse({'name': obj.name,
                                 'col_sep': obj.column_separator,
                                 'str_char': obj.string_character,
                                 'id': obj.pk,
                                 'columns': col})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


@login_required()
def editing_schema(request, pk):
    """Editing schema page"""

    schema = Schema.objects.get(id=pk)
    columns = ColumnItem.objects.filter(schema=pk)
    data = {
        'schema': schema,
        'columns': columns,
    }
    return render(request, 'main/editing_schema.html', data)


def edit_req(request):
    """Saving edited data"""

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            schema = Schema.objects.get(id=data["id"])
            schema.name = data['name']
            schema.column_separator = data['col_sep']
            schema.string_character = data['str_char']
            schema.updated = datetime.datetime
            schema.is_created = False
            schema.save()
            schema_cols = ColumnItem.objects.filter(schema=schema.id)
            for sc_col in schema_cols:
                sc_col.delete()
            for col in data['columns']:
                new_col = ColumnItem()
                new_col.col_name = col['col_name']
                new_col.col_type = col['col_type']
                new_col.order = col['order']
                new_col.user_id = col['c_id']
                if col['col_type'] == 'age':
                    new_col.range_min = col['range_min']
                    new_col.range_max = col['range_max']
                new_col.schema = Schema.objects.get(id=schema.id)
                if new_col.col_name != '' and new_col.order != '':
                    new_col.save()
            return JsonResponse({'status': 200,
                                'id': f'{schema.id}',
                                 'is_created': schema.is_created})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def del_schema(request, id):
    """Delete schema instance"""

    try:
        schema_del = Schema.objects.get(id=id)
        try:
            os.remove(f'{settings.MEDIA_ROOT}/Schema_{schema_del.id}_{schema_del.name}.csv')
        except:
            print('file not found')
        schema_del.delete()
        return HttpResponseRedirect('/')
    except ColumnItem.DoesNotExist:
        return HttpResponseNotFound("<h2>ColumnItem not found</h2>")


@login_required()
def data_sets_view(request, pk):
    """Page with list of schemas in data base"""

    schemas = Schema.objects.all()
    schema = Schema.objects.get(id=pk)
    col_item = ColumnItem.objects.filter(schema=pk)
    data = {
        'schemas': schemas,
        'schema': schema,
        'col_item': col_item,
    }
    return render(request, 'main/data_sets.html', data)


def gen_data(request):
    """Generating csv file"""

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            schema = Schema.objects.get(id=data["id"])
            schema_cols = ColumnItem.objects.filter(schema=schema.id)
            file_name = join(settings.MEDIA_ROOT, f'Schema_{schema.id}_{schema.name}.csv')
            schema.file_link = file_name
            rows_num = int(data['rows'])
            fake = Faker()
            # creating file
            header = []
            gen_flag = False
            for n in schema_cols:
                header.append(n.col_name)

            with open(file_name, 'w') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=schema.column_separator, quotechar=schema.string_character)
                writer.writerow(header)
                for i in range(rows_num):
                    row = []
                    for col in schema_cols:
                        if col.col_type == 'full_name':
                            row.append(fake.name())
                        elif col.col_type == 'phone_number':
                            row.append(fake.phone_number())
                        elif col.col_type == 'address':
                            row.append(fake.address())
                        elif col.col_type == 'job':
                            row.append(fake.job())
                        elif col.col_type == 'company':
                            row.append(fake.company())
                        elif col.col_type == 'age':
                            row.append(random.randint(col.range_min, col.range_max))
                        else:
                            print("type error")
                    writer.writerow(row)
            schema.is_created = True
            schema.save()
            gen_flag = True

            return JsonResponse({'status': 200,
                                 'id': f'{schema.id}',
                                 'is_created': schema.is_created,
                                 'gen_flag': gen_flag,
                                 'link: ': schema.file_link})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')




