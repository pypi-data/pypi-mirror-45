'''
Created on Apr. 28, 2019

@author: jldupont

Performs various operations on NL JSON stdin stream

'''
__version__ = "0.1"

import sys
import click
import json

import jldjson.tools as tools

@click.command()
@click.option('--version', '-v', help="Show version", is_flag=True)
@click.option('--unpack', '-u', help="Unpack a dictionary", multiple=True)
@click.option('--ignore', '-i', help="Ignore error", default=False, is_flag=True)
@click.option('--stderr', help="Errors will be printed to sys.stderr", is_flag=True)
@click.option('--keep', '-k', multiple=True, help="Key to keep in input object")
def command(version, unpack, ignore, stderr, keep):
    """
    Various operators to JSON NL stdin stream
    """
    if version:
        print("Version: ", __version__)
        sys.exit(0)
    
    for line in sys.stdin:
        
        try:
            jobj = tools.loader(line)
            to_unpack = tools.keep(jobj, keep)
            out = tools.unpack(to_unpack, unpack)
                        
        except tools.Skip:
            continue
                        
        except Exception as e:
            out = None
            
            if stderr:
                print("Error: ", str(e), file=sys.stderr)
            
            if ignore == False:
                raise e
            
        if out is None:
            continue

        print(json.dumps(out))
    

if __name__ == '__main__':
    command()