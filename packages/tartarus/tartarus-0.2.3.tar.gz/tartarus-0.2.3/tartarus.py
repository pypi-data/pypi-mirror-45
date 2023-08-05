#!/usr/bin/env python3
import click
import os
import random
import shutil
import gzip
import bz2
import lzma
import zipfile
import base64
import hexrec.xxd


@click.command()
@click.argument('File', type=click.Path(exists=True, resolve_path=True))
@click.option('-o', '--output', default="", help='output file name')
@click.option('-t', default=1, help='How many interations')
@click.option('--gzip', "gz", is_flag=True, default=False, help="Adds Gunzip to operations to be used on file")
@click.option('--bzip2', "b2", is_flag=True, default=False, help="Adds Bzip2 to operations to be used on file")
@click.option('--lzma', "lz", is_flag=True, default=False,  help="Adds lzma to operations to be used on file")
@click.option('--zip', "z", is_flag=True, default=False,  help="Adds Zip to operations to be used on file")
@click.option('--xxd', "x", is_flag=True, default=False, help="Adds xxd (hexdump) to operations to be used on file")
@click.option('--base64', "b64", is_flag=True, default=False, help="Adds base64 encoding to operations to be used on file")
@click.option('--base32', "b32", is_flag=True, default=False, help="Adds base64 encoding to operations to be used on file")
@click.option('--all', is_flag=True, default=False, help="Use all encretion and encoding methods above")
def cli(t, file, output, all, gz, b2, lz, z, x, b64, b32):
    """
    Takes an file and randomly encodes it for obfuscation
    """
    if (output == ""):
        output = os.path.join(os.path.dirname(file), "out")
    tmp = output + ".tmp"

    numOp = 0
    operations = []
    operationLog = []

    if (gz):
        operations.append(EGzip)
    if (b2):
        operations.append(EBZip2)
    if (lz):
        operations.append(ELzma)
    if (z):
        operations.append(EZip)
    if (x):
        operations.append(Exxd)
    if (b64):
        operations.append(EBase64)
    if (b32):
        operations.append(EBase32)
    if(len(operations) == 0 or all == True):
        operations.clear()
        operations = [EGzip, EBZip2, ELzma, EZip, Exxd, EBase64, EBase32]
    copyFile(file, output)
    # start the encode

    for x in range(t):
        ran = random.randint(0, len(operations)-1)
        operationLog.append(ran)
        operations[ran](output, tmp)
        copyFile(tmp, output)

    for x in operationLog:
        print(operations[x])
        pass
    # clean up
    open(tmp, "w")
    os.remove(tmp)


def copyFile(fin, fout):
    """
    Helper function to copy tmp files

    Args:
        fin (path): Path of the input file
        fout (path): Path for the out file
    """
    with open(fin, 'rb') as f_in:
        with open(fout, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def EGzip(fin, fout):
    """
    Helper function to carry out Gunzip

    Args:
        fin (path): Path of the input file
        fout (path): Path for the out file
    """
    with open(fin, 'rb') as f_in:
        with gzip.open(fout, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def EBZip2(fin, fout):
    """
    Helper function to carry out Bzip2

    Args:
        fin (path): Path of the input file
        fout (path): Path for the out file
    """
    with open(fin, 'rb') as f_in:
        with bz2.open(fout, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def ELzma(fin, fout):
    """
    Helper function to carry out Lzma

    Args:
        fin (path): Path of the input file
        fout (path): Path for the out file
    """
    with open(fin, 'rb') as f_in:
        with lzma.open(fout, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def EZip(fin, fout):
    """
    Helper function to carry out zip

    Args:
    fin (path): Path of the input file
    fout (path): Path for the out file
    """
    myzip = zipfile.ZipFile(fout, 'w')
    myzip.write(fin)
    copyFile(fout, fin)


def Exxd(fin, fout):
    """
    Helper function to carry out xxd (ie Hexdump)

    Args:
        fin (path): Path of the input file
        fout (path): Path for the out file
    """
    hexrec.xxd.xxd(fin, fout)


def EBase64(fin, fout):
    """
    Helper function to carry out base64 encoding

    Args:
        fin (path): Path of the input file
        fout (path): Path for the out file
    """
    inFile = open(fin, 'rb').read()
    outFile = open(fout, 'wb')
    outFile.write(base64.b64encode(inFile))


def EBase32(fin, fout):
    """
    Helper function to carry out base32 encoding

    Args:
        fin (path): Path of the input file
        fout (path): Path for the out file
    """
    inFile = open(fin, 'rb').read()
    outFile = open(fout, 'wb')
    outFile.write(base64.b32encode(inFile))
