#!/usr/bin/env python3

import os
import shutil
import click
from .param_parser import parse_json
from .transformers import Jinja2Transformer

@click.group()
def cli():
    '''
    CopyPasta

    Simple scaffolding using Jinja2 templates
    '''
    pass


def mkdir_ifnotexists(path):
    if not os.path.exists(path):
        os.mkdir(path)


# TODO Max dir level nesting?
def copy_dir_structure(src, dst, params={}):
    t = Jinja2Transformer()
    src, dst = os.path.abspath(src), os.path.abspath(dst)
    print(f'CopyPasta from {src} to {dst}')
    # Copy similar directory structure to destination, substituting any variable names
    mkdir_ifnotexists(dst)
    for src_root, dirnames, filenames in os.walk(src):
        print(f'Transforming files under {src_root}')
        # Trim away len(src)+1 characters to get path relative to src and dst. +1 is to remove leading slash
        dir_root = src_root[len(src) + 1:]
        for dirname in dirnames:
            dst_path = os.path.join(dst, dir_root, dirname)
            # TODO this might not be always desirable
            dst_path = t.transform_string(dst_path, params)
            if os.path.isfile(dst_path):
                raise Exception(
                    f"Failed to create directory at {dirname} due to existing file"
                )
            mkdir_ifnotexists(dst_path)

        for filename in filenames:
            dst_path = os.path.join(dst, dir_root, filename)
            src_path = os.path.join(src_root, filename)
            extension = os.path.splitext(src_path)[-1]
            if extension in t.file_extensions:
                print(f'Transforming {filename}...')
                t.transform(src_path, dst_path, params)
            else:
                print(f'Copying {filename}...')
                shutil.copy(src_path, dst_path)


JSON_PARAM_FILE = 'config.json'


@cli.command(
    help=
    '''
    Copies directory structure and files from `template_path` to `output_path`,
    transforming any Jinja2 template files (.j2) it sees
    '''
)
@click.argument('template_path')
@click.argument('output_path')
@click.option(
    '--config_file',
    help='Path to config.json to configure variables in templates',
    default='./config.json')
def copy(template_path, output_path, config_file):
    # Get any variables
    params = {}
    if os.path.exists(config_file) and os.path.isfile(config_file):
        params = parse_json('config.json')

    # Transform src to dst using variables
    copy_dir_structure(template_path, output_path, params)

if __name__ == '__main__':
    cli()
