# -*- coding: utf-8 -*-
from __future__ import division, print_function

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import os
import pathlib
import socket
import math
import tarfile
import tempfile
import argparse
import streamer_utils as su
from config import log

# MOOSE uses first 9 bytes to encode the length of message.
prefixL_ = 9

def gen_prefix(msg, maxlength=9):
    msg = '>%s' % msg
    if len(msg) < maxlength:
        msg += ' ' * (maxlength - len(msg))
    return msg[:maxlength].encode( 'utf-8' )

def write_data_to_socket(conn, msg):
    global prefixL_
    prefix = b'0'*(prefixL_- int(math.log10(len(msg)))-1) + b'%d' % len(msg)
    assert len(prefix) == prefixL_
    msg = b'%s%s' % (prefix, msg)
    conn.sendall(msg)

def gen_payload( args ):
    path = args['main_file']
    if not path:
        raise RuntimeError( 'No input fie' )
    if not pathlib.Path(path).is_file():
        raise RuntimeError( "File %s not found." % path )
        
    archive = pathlib.Path(tempfile.mkdtemp()) / 'data.tar.bz2'

    # This mode (w|bz2) is suitable for streaming. The blocksize is default to
    # 20*512 bytes. We change this to 2048
    with tarfile.open(archive, 'w|bz2', bufsize=2048 ) as h:
        p = pathlib.Path(path)
        if p.is_file():
            h.add(path, p.name)
        else:
            h.add(path)
        # add other files.
        for f in args['other_files'].split(';'):
            h.add(f, pathlib.Path(f).name) if f else None

    with open(archive, 'rb') as f:
        data = f.read()
    return data

def get_n_bytes(conn, n):
    data = b''
    while len(data) < n:
        data += conn.recv(n-len(data), socket.MSG_WAITALL)
    return data

def read_msg(conn):
    global prefixL_
    # first get the first 9 byes
    nBytes = get_n_bytes(conn, prefixL_)
    nBytes = int(nBytes)
    data = get_n_bytes(conn, nBytes)
    # prefix is <ABC> followed by data'
    assert data[0] == ord(b'<'), (data[0], data[:10])
    assert data[4] == ord(b'>'), (data[4], data[:10])
    return data[1:4], data[5:] 

def save_bz2(conn, outfile):
    # first 9 bytes always tell how much to read next. Make sure the submit job
    # script has it
    prefix, data = read_msg(conn)
    assert prefix == b'TAR', 'Invalid prefix for TAR data'
    with open(outfile, 'wb') as f:
        f.write(data)
    print( "[INFO ] Got total %d bytes." % len(data) )
    return data

def main( args ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host, port = args['server'].rsplit(':', 1)
        sock.connect( (host, int(port)) )
        log('[INFO] Connected with %s:%s'%(host,port))
    except Exception as e:
        print( "[ERROR] Failed to connect to %s. Error %s "%(args['server'],e))
        return None

    sock.settimeout(10)
    data = b''
    try:
        data += gen_payload( args )
    except Exception as e:
        log( "[ERROR] Failed to generate payload. Error: %s"%e)
        return None

    write_data_to_socket(sock, data)
    log( "[INFO ] Total data sent : %d bytes " % len(data) )

    # This is response from the server.
    tableData = b''
    while True:
        d = b''
        try:
            prefix, d = read_msg(sock)
        except socket.timeout:
            continue

        if prefix == b'TAB':
            log("[INFO] Time to stream table data.")
            tableData += d
            decoded, tableData = su.decode_data(tableData)
            print(decoded, len(tableData), chr(tableData[0]))
        elif prefix == 'EOS':
            log("[INFO] End of simulation.")
            break
    
    outfile = os.path.join(tempfile.mkdtemp(), 'res.tar.bz2')
    data = save_bz2(sock, outfile)
    return data, outfile

def submit_job(data):
    assert data['main_file'], 'Empty file name'
    return main(data)

if __name__ == '__main__':
    # Argument parser.
    description = '''Submit a job to moose server.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('path', metavar='path'
        , help = 'File or directory to execute on server.'
        )
    parser.add_argument('--main', '-m', nargs = '+'
        , required = False, default = []
        , help = 'In case of multiple files, scripts to execute'
                ' on the server, e.g. -m file1.py -m file2.py.'
                ' If not given, server will try to guess the best option.'
        )
    parser.add_argument('--server', '-s'
        , required = False, type=str, default='localhost:31417'
        , help = 'IP address and PORT number of moose server e.g.'
                 ' 172.16.1.2:31416'
        )
    class Args: pass
    args = Args()
    parser.parse_args(namespace=args)
    main( vars(args) )
