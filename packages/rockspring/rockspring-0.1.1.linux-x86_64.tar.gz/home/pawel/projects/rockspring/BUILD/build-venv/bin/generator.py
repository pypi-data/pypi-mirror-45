import click
import hashlib
import jinja2 as j
import json
import os
import pkg_resources
import re


def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def create_cpp_model(model):
    simple_type_map = {
        'uint64': 'uint64_t',
        'uint32': 'uint32_t',
        'boolean': 'bool',
        'float': 'float'
    }

    def _map_field(field):
        kind = ''
        getter_type = ''
        internal_type = ''
        list_by_value = False
        list_type = ''
        type_in_struct = ''

        if field['type'] in simple_type_map and 'repeated' not in field:
            kind = 'simple'
            type_in_struct = getter_type = simple_type_map[field['type']]
        elif field['type'] == 'string' and 'repeated' not in field:
            kind = 'string'
            type_in_struct = 'rs::Array'
        elif 'repeated' in field and field['type'] != 'string':
            kind = 'list'
            getter_type = simple_type_map[field['type']] if field['type'] in simple_type_map else field['type']
            internal_type = simple_type_map[field['type']] if field['type'] in simple_type_map else '_::__' + field['type']
            list_by_value = field['type'] in simple_type_map
            list_type = 'ValueList' if list_by_value else 'List'
            type_in_struct = 'rs::Array'
        elif 'repeated' not in field:
            kind = 'reference'
            getter_type = field['type']
            type_in_struct = internal_type = '_::__' + field['type']
        else:
            raise Exception('Unsupported type combination: ' + str(field))

        return {
            'name': field['name'],
            'name_in_struct': field['name'],
            'type_in_struct': type_in_struct,
            'property_name': field['name'][0].capitalize() + field['name'][1:],
            'getter': 'Is' if field['type'] == 'boolean' else 'Get',
            'getter_type': getter_type,
            'internal_type': internal_type,
            'list_by_value': list_by_value,
            'list_type': list_type,
            'kind': kind,
        }

    def _map_message(msg):
        return {
            'class_name': msg['name'],
            'struct_name': '__' + msg['name'],
            'struct_ref_name': '_::__' + msg['name'],
            'fields': [_map_field(f) for f in msg['fields']]
        }

    def _map_method(method, service):
        return {
            'name': method['name'],
            'has_reply': 'reply' in method,
            'reply': method['reply'] if 'reply' in method else '',
            'request': method['request'],
            'method_id': '0x' + hashlib.md5(service['name'] + method['name']).hexdigest()[0:16]
        }

    def _map_service(service):
        return {
            'name': service['name'],
            'methods': [_map_method(m, service) for m in service['methods']],
            'var_name': to_snake_case(service['name'])
        }

    return {
        'name': model['name'][0].upper() + model['name'][1:],
        'dto_header': model['name'] + '.dto.h',
        'services_header': model['name'] + '.services.h',
        'listener_header': model['name'] + '.listener.h',
        'listener_source': model['name'] + '.listener.cc',
        'file_id': model['name'].upper(),
        'namespace': model['namespace'],
        'messages': [_map_message(m) for m in model['messages']],
        'services': [_map_service(s) for s in model['services']]
    }


def create_pxd_model(model):
    return create_cpp_model(model)


def create_pyx_model(model):
    cpp_model = create_cpp_model(model)

    for m in cpp_model['messages']:
        m['dto_name'] = 'Dto' + m['class_name']

        for f in m['fields']:
            f['python_name'] = to_snake_case(f['name'])
            f['python_type'] = 'list' if f['kind'] == 'list' else 'string' if f['kind'] == 'string' else f['getter_type']
            f['doc_type'] = 'list of ' + f['getter_type'] if f['kind'] == 'list' else 'string' if f['kind'] == 'string' else f['getter_type']
    
    for s in cpp_model['services']:
        s['python_var_name'] = to_snake_case(s['name'])

        for m in s['methods']:
            m['python_name'] = to_snake_case(m['name'])

    return cpp_model


def create_setup_model(model, include_dirs):
    model['include_dirs'] = include_dirs
    return model


def generate_template(template, output_file, model):
    template = j.Template(template)
    
    with open(output_file, 'w+') as f:
        f.write(template.render(model))


def read_file(file_name):
    with open(file_name) as f:
        return f.read()


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def read_template(template):
    return pkg_resources.resource_string(__name__, 'templates/' + template + '.jinja2')


@click.command()
@click.option('--config', required=True, help='File with service definitions')
@click.option('--include-dirs', default='', required=False, help='":" separated list of additional directories for include of header files and libraries')
@click.option('--cxx-out', required=True, help='C++ server side code output directory')
@click.option('--cython-out', required=True, help='Cython client code output directory')
def generate(config, include_dirs, cxx_out, cython_out):
    model = json.loads(read_file(config))
    
    include_dirs = [os.path.abspath(x) for x in include_dirs.split(':') + [cxx_out] + [cython_out]]
    name = model['name']

    mkdir(cxx_out)
    mkdir(cython_out)

    cpp_model = create_cpp_model(model)

    generate_template(
        read_template('dto.h'),
        os.path.join(cxx_out, cpp_model['dto_header']),
        cpp_model)

    generate_template(
        read_template('services.h'),
        os.path.join(cxx_out, cpp_model['services_header']),
        cpp_model)

    generate_template(
        read_template('listener.h'),
        os.path.join(cxx_out, cpp_model['listener_header']),
        cpp_model)
    
    generate_template(
        read_template('listener.cc'),
        os.path.join(cxx_out, cpp_model['listener_source']),
        cpp_model)

    generate_template(
        read_template('cpp_wrapper.pxd'),
        os.path.join(cython_out, 'cpp_wrapper.pxd'),
        create_pxd_model(model))

    generate_template(
        read_template('client.pyx'),
        os.path.join(cython_out, name + '.pyx'),
        create_pyx_model(model))

    generate_template(
        read_template('setup.py'),
        os.path.join(cython_out, 'setup.py'),
        create_setup_model(model, include_dirs))

