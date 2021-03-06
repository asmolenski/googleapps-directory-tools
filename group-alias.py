#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import pprint
import argparse

from const import *
from utils import *

def show_resource(resource):
    if resource.has_key('primaryEmail'):
        print "primaryEmail: %s" % resource['primaryEmail']
    print "alias:        %s" % resource['alias']

def show_resource_list(resources, verbose):
    if resources.has_key('aliases'):
        for resource in resources['aliases']:
            if verbose:
                show_resource(resource)
                print ""
            else:
                print "%s %s" % (resource['primaryEmail'], resource['alias'])

def list_alias(sv, args):
    status, r = execute_admin_api(sv.list(groupKey=args.groupKey))
    if status == 404:
        sys.stderr.write('%s does not exist\n' % args.groupKey)
        sys.exit(2)
    if args.jsonPretty:
        print to_pretty_json(r)
    elif args.json:
        print to_json(r)
    else:
        show_resource_list(r, args.verbose)

def insert_alias(sv, args):
    body = { 'alias': args.alias }
    status, r = execute_admin_api(sv.insert(groupKey=args.groupKey, body=body))
    if status == 404:
        sys.stderr.write('%s does not exist\n' % args.groupKey)
        sys.exit(2)
    if args.verbose:
        if args.jsonPretty:
            print to_pretty_json(r)
        elif args.json:
            print to_json(r)
        else:
            show_resource(r)

def delete_alias(sv, args):
    status, r = execute_admin_api(sv.delete(groupKey=args.groupKey, alias=args.alias))

def main():
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    subparsers = parser.add_subparsers(help='sub command')

    #-------------------------------------------------------------------------
    # LIST
    #-------------------------------------------------------------------------
    parser_list = subparsers.add_parser('list', help='Lists all aliases for a group')
    parser_list.add_argument('groupKey', help='group email address, aliase or unique id')
    parser_list.add_argument('-v', '--verbose', action='store_true', help='show group all alias data')
    parser_list.add_argument('--json', action='store_true', help='output in JSON')
    parser_list.add_argument('--jsonPretty', action='store_true', help='output in pretty JSON')
    parser_list.set_defaults(func=list_alias)

    #-------------------------------------------------------------------------
    # INSERT
    #-------------------------------------------------------------------------
    parser_insert = subparsers.add_parser('insert', help='Adds an alias for the group')
    parser_insert.add_argument('groupKey', help='group email address, aliase or unique id')
    parser_insert.add_argument('alias', help='alias email address')
    parser_insert.add_argument('-v', '--verbose', action='store_true', help='show created alias data')
    parser_insert.add_argument('--json', action='store_true', help='output in JSON')
    parser_insert.add_argument('--jsonPretty', action='store_true', help='output in pretty JSON')
    parser_insert.set_defaults(func=insert_alias)

    #-------------------------------------------------------------------------
    # DELETE
    #-------------------------------------------------------------------------
    parser_delete = subparsers.add_parser('delete', help='Removes an alias')
    parser_delete.add_argument('groupKey', help='group email address, aliase or unique id')
    parser_delete.add_argument('alias', help='alias email address')
    parser_delete.set_defaults(func=delete_alias)

    args = parser.parse_args()
    
    service = get_directory_service(args)

    args.func(service.groups().aliases(), args)


if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    main()
