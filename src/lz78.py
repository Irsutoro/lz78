#!/usr/bin/env python3
"""LZ78 (de)compression algorithm."""

import itertools
import math


BYTEORDER = 'big'


def encode(data):
    """Encode data using LZ78 compression.

    Args:
        data: A str to encode.

    Returns:
        A list of two-element tuples of int and str.
    """
    dictionary = {}
    index = itertools.count(1)
    word = ''
    result = []
    for character in data:
        new_word = word + character
        if new_word not in dictionary:
            result.append((dictionary.get(word, 0), character))
            dictionary[new_word] = index.__next__()
            word = ''
        else:
            word = new_word
    # Corner-case: without this resulting list will be incomplete
    if word:
        result.append((dictionary.get(word[:-1], 0), word[-1:]))
    return result


def decode(encoded_data):
    """Decode encoded data using LZ78 decompression.

    Args:
        encoded_data: A list of two-element tuples of int and str.

    Returns:
        A str.
    """
    dictionary = {}
    index = itertools.count(1)
    result = ''
    for i, character in encoded_data:
        word = dictionary.get(i, '') + character
        result += word
        dictionary[index.__next__()] = word
    return result


def to_file(encoded_data, filename):
    """Write encoded data to the binary file.

    Args:
        encoded_data: A list of two-element tuples of int and str.
        filename: Name of the destination file.
    """
    required_bytes = math.ceil(
        len(bin(max([i[0] for i in encoded_data]))[2:]) / 8)
    bytes_ = b''.join([i.to_bytes(length=required_bytes, byteorder=BYTEORDER)
                       + character.encode() for i, character in encoded_data])
    with open(filename, 'wb') as file:
        file.write(required_bytes.to_bytes(length=1, byteorder=BYTEORDER))
        file.write(bytes_)


def from_file(filename):
    """Read encoded data from the binary file.

    Args:
        filename: Name of the source file.

    Returns:
        A list of two-element tuples of int and str.
    """
    with open(filename, 'rb') as file:
        required_bytes = int.from_bytes(file.read(1), byteorder=BYTEORDER)
        bytes_ = file.read()
    result = []
    chunk_size = required_bytes + 1
    chunks = [bytes_[r:r+chunk_size]
              for r in range(0, len(bytes_), chunk_size)]
    for chunk in chunks:
        i = int.from_bytes(chunk[:required_bytes], byteorder=BYTEORDER)
        character = chunk[-1:].decode()
        result.append((i, character))
    return result


def hardcoded():
    dataset = [
        'abbbcaabbcbbcaaac',
        3 * 'a',
        # Examples of corner-case {
        4 * 'a',
        5 * 'a',
        6 * 'a',
        # }
        7 * 'a',
    ]
    for data in dataset:
        print(f'data to encode: {data}')
        encoded = encode(data)
        print(f'encoded: {encoded}')
        print(f'decoded == data: {decode(encoded) == data}')
        filename = f'{data}.lz78'
        to_file(encoded, filename)
        encoded_from_file = from_file(filename)
        print(f'encoded == encoded_from_file: {encoded == encoded_from_file}')
        print(encoded_from_file)
        print()


def hardcoded_file():
    input_filename = 'a.txt'
    output_filename = 'a.txt.lz78'
    with open(input_filename, 'r') as file:
        input_ = file.read()
    to_file(encode(input_), output_filename)

    decompressed = decode(from_file(output_filename))
    print(decompressed, end='')


def interactive():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    parser.add_argument('-d', '--decompress', action='store_true')
    args = parser.parse_args()
    if not args.decompress:
        with open(args.input_file, 'r') as file:
            input_ = file.read()
        to_file(encode(input_), args.output_file)
    else:
        decompressed = decode(from_file(args.input_file))
        with open(args.output_file, 'w') as file:
            file.write(decompressed)


def main():
    # hardcoded()
    # hardcoded_file()
    interactive()


if __name__ == '__main__':
    main()
