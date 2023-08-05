#!/usr/bin/env python3
import click
import os
import random
import shutil
import gzip
import bz2
import lzma
import zipfile
import hexrec.xxd


@click.command()
@click.argument('File', type=click.Path(exists=True, resolve_path=True))
@click.option('-o', '--output', default="", help='output file name')
@click.option('-t', default=1, help='How many interations')
@click.option('--gzip', "gz", is_flag=True, default=False)
@click.option('--bzip2', "b2", is_flag=True, default=False)
@click.option('--lzma', "lz", is_flag=True, default=False)
@click.option('--zip', "zip", is_flag=True, default=False)
@click.option('--xxd', "xxd", is_flag=True, default=False)
@click.option('--all', is_flag=True, default=False, help="Use all encretion and encoding methods above")
def cli(t, file, output, all, gz, b2, lz, zip, xxd):
    if (output == ""):
        output = os.path.join(os.path.dirname(file), "out")
    tmp = output + ".tmp"

    numOp = 0
    operations = []
    operationLog = []

    if (gz == True):
        operations.append(Egzip)
    if (b2 == True):
        operations.append(Ebzip2)
    if (lz == True):
        operations.append(Elzma)
    if (zip == True):
        operations.append(Ezip)
    if (xxd == True):
        operations.append(Exxd)
    if(len(operations) == 0 or all == True):
        operations.clear()
        operations = [Egzip, Ebzip2, Elzma, Ezip, Exxd]
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
    with open(fin, 'rb') as f_in:
        with open(fout, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def Egzip(fin, fout):
    with open(fin, 'rb') as f_in:
        with gzip.open(fout, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def Ebzip2(fin, fout):
    with open(fin, 'rb') as f_in:
        with bz2.open(fout, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def Elzma(fin, fout):
    with open(fin, 'rb') as f_in:
        with lzma.open(fout, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def Ezip(fin, fout):
    myzip = zipfile.ZipFile(fout, 'w')
    myzip.write(fin)
    copyFile(fout, fin)


def Exxd(fin, fout):
    hexrec.xxd.xxd(fin, fout)
