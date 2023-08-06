#!/usr/bin/env python
import os
from optparse import OptionParser

FILES = {}


def write_to_file(filename, line, tmpdir='./tmp'):
    """
    return True

    This functions writes the line into the filename.

    :param filename:   Filename to write the line.
    :param line:       Line to write it temporary file.
    :param tmpdir:     Temporary work directory.

    """
    line = line.strip()
    if line != '':
        if filename not in FILES:
            fq = open(filename, 'a')
            FILES[filename] = fq
        FILES[filename].write(line + '\n')
    return True


def get_filename(line, tmpdir='./tmp'):
    """
    return <filename>

    This function returns the filename where the line should
    be saved.

    :param line:       Line to take the first two letters to
                       write split files.
    :param tmpdir:     Temporary work directory.
    """
    line = line.strip()
    file_name = line[:2]
    f = '%s/%s' % (tmpdir, file_name)
    return f


def split_file(filename, block_size, tmpdir='./tmp'):
    """
    return True

    This function reads the big file and split it in small
    sorted blocks in the temporary directory.

    :param filename:   Filename to split in small blocks.
    :param block_size: Block size.
    :param tmpdir:     Temporary work directory.

    """
    f = open(filename, 'r')
    while True:
        lines = f.readlines(block_size)
        if lines == []:
            break
        lines.sort()
        for line in lines:
            file_name = get_filename(line, tmpdir)
            write_to_file(file_name, line)
    f.close()
    for f in FILES:
        FILES[f].close()
    return True


def tmp_exists(tmpdir):
    """
    return True

    Check if the temporary directory exists and if not will
    create the directory.

    :param tmpdir:     Temporary work directory.

    """
    if not os.path.exists(tmpdir) or not os.path.isdir(tmpdir):
        os.makedirs(tmpdir)
    return True


def tmp_purge(tmpdir):
    """
    return True

    This function will remove the temporary directory.

    :param tmpdir:     Temporary work directory.

    """
    files = os.listdir('%s/' % (tmpdir))
    for f in files:
        os.remove('%s/%s' % (tmpdir, f))
    os.rmdir(tmpdir)
    return True


def sortfile(filename, block_size=104857600,
             tmpdir='./tmp', output='out.txt'):
    """
    returns True

    This function is to sort big files, split them in small
    blocks using the first two letters of the line.

    :param filename:   Filename to sort.
    :param block_size: Block size.
    :param tmpdir:     Temporary work directory.
    :param output:     Output filename.

    """
    tmp_exists(tmpdir)
    if os.path.exists(output) and os.path.isfile(output):
        os.remove(output)
    split_file(filename, block_size, tmpdir)
    files = os.listdir('%s/' % (tmpdir))
    files.sort()
    out_file = open(output, 'a', block_size)
    for f in files:
        fd = open('%s/%s' % (tmpdir, f))
        lines = fd.readlines()
        lines.sort()
        for i in lines:
            out_file.write(i)
        fd.close()
    out_file.close()
    tmp_purge(tmpdir)
    return True


def run(options):
    """
    return <bool>

    This function will run the sortfile with parameters.

    :param options:    Dictionary with following keys:
                       (output, filename, tmpdir, block_size)

    """
    if 'filename' in options:
        return sortfile(**options)
    return False


def main():
    parser = OptionParser(usage="usage: %prog [action] [options]",
                          version="%prog 0.0.1")
    parser.add_option("-b", "--blocksize", dest="block_size",
                      default=104857600, type=int,
                      help="Block size.")
    parser.add_option("-f", "--filename", dest="filename",
                      help="Filename to sort.")
    parser.add_option("-o", "--output", dest="output",
                      default="out.txt",
                      help="Output filename.")
    parser.add_option("-t", "--tmpdir", dest="tmpdir",
                      default="./tmp",
                      help="Temporary directory.")

    (options, args) = parser.parse_args()
    if not run(vars(options)):
        print("Required arguments missing or invalid.")
        print(parser.print_help())


if __name__ == '__main__':
    main()
