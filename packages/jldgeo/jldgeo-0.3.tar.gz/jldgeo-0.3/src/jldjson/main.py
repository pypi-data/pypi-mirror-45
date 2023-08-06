'''
Created on Apr. 28, 2019

@author: jldupont

Performs various operations on NL JSON stdin stream

'''
import sys
import click
import json

@click.command()
@click.option('--ignore', '-i', help="Ignore error", default=False, is_flag=True)
@click.option('--stderr', help="Errors will be printed to sys.stderr", is_flag=True)
@click.option('--keep', '-k', multiple=True, help="Key to keep in input object")
def command(ignore, stderr, keep):
    
    for line in sys.stdin:
        
        line = " ".join(line.split())
        
        try:
            jobj = json.loads(line)
            
        except:
            jobj = None
            
            if stderr:
                print("Expecting JSON object, got:", line, file=sys.stderr)
            
            if ignore == False:
                raise Exception("Expecting JSON object")
            

        if jobj is None:
            continue

        out = {}

        for item in keep:
            if item in jobj:
                out[item] = jobj[item]
                
        print(json.dumps(out))
    

if __name__ == '__main__':
    command()