# coding: utf-8
import argparse
import codecs
import importlib
import inspect
import json
import os
import sys
import yaml

from jinja2 import Environment, PackageLoader, FileSystemLoader, TemplateError

from swg2rst.converter_exceptions import ConverterError


def main(from_script=True):

    from_stdin = from_script and not sys.stdin.isatty()

    if sys.version_info.major == 2:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    parser = argparse.ArgumentParser(
        description='Convert "Swagger" format file to "Restructured text"')

    if not from_stdin:
        parser.add_argument(
            'path', metavar='path', type=str, help='Path to swagger file')
    parser.add_argument(
        '-f', '--format', type=str, help='Format output doc file (rst)', required=True)
    parser.add_argument(
        '-d', '--destination-path', type=str, help='Folder for saving file')
    parser.add_argument(
        '-t', '--template', type=str, help='Path to custom template file')
    parser.add_argument(
        '-e', '--examples', type=str, help='Path to custom examples file (yaml or json)')
    parser.add_argument(
        '-i', '--inline',
        action='store_true',
        help='Output definitions locally in paths, otherwise in isolated section')

    args = parser.parse_args()
    available_formats = ('rst',)

    if args.format not in available_formats:
        sys.exit('Invalid output format')

    doc_module = importlib.import_module('swg2rst.utils.{}'.format(args.format))

    _file = sys.stdin if from_stdin else _open_file(args.path)

    try:
        doc = _parse_file(_file)
    except ValueError:
        sys.exit('Invalid file format. File must be in "yaml" or "json" format.')
    finally:
        if not from_stdin:
            _file.close()

    if doc is None:
        sys.exit('File is empty')

    examples = None
    if args.examples:
        with _open_file(args.examples) as _file:
            try:
                examples = _parse_file(_file)
            except ValueError:
                sys.exit('Invalid examples file format. File must be in "yaml" or "json" format.')
            else:
                if examples is None:
                    sys.exit('Examples file is empty')

    try:
        swagger_doc = doc_module.SwaggerObject(doc, examples=examples)
    except ConverterError as err:
        sys.exit(err)

    jinja_env = Environment(lstrip_blocks=True, trim_blocks=True)

    for name, function in inspect.getmembers(doc_module, inspect.isfunction):
        jinja_env.filters[name] = function
    jinja_env.filters['json_dumps'] = json.dumps

    if args.template:
        jinja_env.loader = FileSystemLoader(os.path.dirname(args.template))
        template = jinja_env.get_template(os.path.basename(args.template))
    else:
        jinja_env.loader = PackageLoader('swg2rst')
        try:
            template = jinja_env.get_template('basic.{}'.format(args.format))
        except TemplateError as err:
            sys.exit(u'Template Error: {}'.format(err.message))

    result_filename = from_stdin and 'doc' or args.path.split('/')[-1].split('.')[0]
    try:
        rst_doc = template.render(
            doc=swagger_doc, filename=result_filename, inline=args.inline)
    except (ConverterError, TemplateError) as err:
        status = err
        if isinstance(err, TemplateError):
            status = 'Template Error: {}'.format(err)
        sys.exit(status)

    if args.destination_path:
        result_file_path = '{}/{}.{}'.format(
            os.path.normpath(args.destination_path),
            result_filename,
            args.format
        )

        with codecs.open(result_file_path, mode='w', encoding='utf-8') as f:
            f.write(rst_doc)
            print('\n\nResult saved to %s' % os.path.abspath(result_file_path))

    else:
        print(rst_doc)

def _parse_file(_file):
    try:
        doc = yaml.load(_file)
    except ValueError:
        doc = json.load(_file)

    return doc


def _open_file(path):
    return codecs.open(path, 'r', encoding='utf-8')


if __name__ == '__main__':
    main(False)
