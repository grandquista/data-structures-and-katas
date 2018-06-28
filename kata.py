from functools import lru_cache
from re import search, split
from typing import Iterable

LIMIT = 4

SOLUTION_ODD = {
    1: '[01]+',
    3:
        '10101|1001',
    5:
        '1110111111011|1110111110001|1110111100111|1110111010011|1110111001001'
        '|1110110101011|1110110100001|1110110010111|1110110000011'
        '|1110101011011|1110101010001|1110101000111|1110100110011'
        '|1110100101001|1110100001011|1110100000001|1110010111011'
        '|1110010110001|1110010100111|1110010010011|1110010001001'
        '|1110001101011|1110001100001|1110001010111|1110001000011'
        '|1110000011011|1110000010001|1110000000111|1101101111011'
        '|1101101110001|1101101100111|1101101010011|1101101001001'
        '|1101100101011|1101100100001|1101100010111|1101100000011'
        '|1101011011011|1101011010001|1101011000111|1101010110011'
        '|1101010101001|1101010001011|1101010000001|1101000111011'
        '|1101000110001|1101000100111|1101000010011|1101000001001'
        '|1100011111011|1100011110001|1100011100111|1100011010011'
        '|1100011001001|1100010101011|1100010100001|1100010010111'
        '|1100010000011|1100001011011|1100001010001|1100001000111'
        '|1100000110011|1100000101001|1100000001011|1100000000001'
        '|1001111111011|1001111110001|1001111100111|1001111010011'
        '|1001111001001|1001110101011|1001110100001|1001110010111'
        '|1001110000011|1001101011011|1001101010001|1001101000111'
        '|1001100110011|1001100101001|1001100001011|1001100000001'
        '|1001010111011|1001010110001|1001010100111|1001010010011'
        '|1001010001001|1001001101011|1001001100001|1001001010111'
        '|1001001000011|1001000011011|1001000010001|1001000000111'
        '|1000101111011|1000101110001|1000101100111|1000101010011'
        '|1000101001001|1000100101011|1000100100001|1000100010111'
        '|1000100000011|1000011011011|1000011010001|1000011000111'
        '|1000010110011|1000010101001|1000010001011|1000010000001'
        '|1000000111011|1000000110001|1000000100111|1000000010011'
        '|1000000001001|111011111011|111011110001|111011100111|111011010011'
        '|111011001001|111010101011|111010100001|111010010111|111010000011'
        '|111001011011|111001010001|111001000111|111000110011|111000101001'
        '|111000001011|111000000001|110110111011|110110110001|110110100111'
        '|110110010011|110110001001|110101101011|110101100001|110101010111'
        '|110101000011|110100011011|110100010001|110100000111|110001111011'
        '|110001110001|110001100111|110001010011|110001001001|110000101011'
        '|110000100001|110000010111|110000000011|100111111011|100111110001'
        '|100111100111|100111010011|100111001001|100110101011|100110100001'
        '|100110010111|100110000011|100101011011|100101010001|100101000111'
        '|100100110011|100100101001|100100001011|100100000001|100010111011'
        '|100010110001|100010100111|100010010011|100010001001|100001101011'
        '|100001100001|100001010111|100001000011|100000011011|100000010001'
        '|100000000111|11101111011|11101110001|11101100111|11101010011'
        '|11101001001|11100101011|11100100001|11100010111|11100000011'
        '|11011011011|11011010001|11011000111|11010110011|11010101001'
        '|11010001011|11010000001|11000111011|11000110001|11000100111'
        '|11000010011|11000001001|10011111011|10011110001|10011100111'
        '|10011010011|10011001001|10010101011|10010100001|10010010111'
        '|10010000011|10001011011|10001010001|10001000111|10000110011'
        '|10000101001|10000001011|10000000001|1110111011|1110110001|1110100111'
        '|1110010011|1110001001|1101101011|1101100001|1101010111|1101000011'
        '|1100011011|1100010001|1100000111|1001111011|1001110001|1001100111'
        '|1001010011|1001001001|1000101011|1000100001|1000010111|1000000011'
        '|111011011|111010001|111000111|110110011|110101001|110001011'
        '|110000001|100111011|100110001|100100111|100010011|100001001|11101011'
        '|11100001|11010111|11000011|10011011|10010001|10000111|1110011'
        '|1101001|1001011|1000001|110111|100011|11001|1111',
    7:
        '1101111111001|1101111101011|1101111011101|1101111000001|1101110110011'
        '|1101110100101|1101110001001|1101101111011|1101101101101'
        '|1101101010001|1101101000011|1101100011001|1101100001011'
        '|1101011111101|1101011100001|1101011010011|1101011000101'
        '|1101010101001|1101010011011|1101010001101|1101000111001'
        '|1101000101011|1101000011101|1101000000001|1100111110011'
        '|1100111100101|1100111001001|1100110111011|1100110101101'
        '|1100110010001|1100110000011|1100101011001|1100101001011'
        '|1100100111101|1100100100001|1100100010011|1100100000101'
        '|1100001111001|1100001101011|1100001011101|1100001000001'
        '|1100000110011|1100000100101|1100000001001|1011111111011'
        '|1011111101101|1011111010001|1011111000011|1011110011001'
        '|1011110001011|1011101111101|1011101100001|1011101010011'
        '|1011101000101|1011100101001|1011100011011|1011100001101'
        '|1011010111001|1011010101011|1011010011101|1011010000001'
        '|1011001110011|1011001100101|1011001001001|1011000111011'
        '|1011000101101|1011000010001|1011000000011|1010011111001'
        '|1010011101011|1010011011101|1010011000001|1010010110011'
        '|1010010100101|1010010001001|1010001111011|1010001101101'
        '|1010001010001|1010001000011|1010000011001|1010000001011'
        '|1001111111101|1001111100001|1001111010011|1001111000101'
        '|1001110101001|1001110011011|1001110001101|1001100111001'
        '|1001100101011|1001100011101|1001100000001|1001011110011'
        '|1001011100101|1001011001001|1001010111011|1001010101101'
        '|1001010010001|1001010000011|1001001011001|1001001001011'
        '|1001000111101|1001000100001|1001000010011|1001000000101'
        '|1000101111001|1000101101011|1000101011101|1000101000001'
        '|1000100110011|1000100100101|1000100001001|1000011111011'
        '|1000011101101|1000011010001|1000011000011|1000010011001'
        '|1000010001011|1000001111101|1000001100001|1000001010011'
        '|1000001000101|1000000101001|1000000011011|1000000001101|110111111001'
        '|110111101011|110111011101|110111000001|110110110011|110110100101'
        '|110110001001|110101111011|110101101101|110101010001|110101000011'
        '|110100011001|110100001011|110011111101|110011100001|110011010011'
        '|110011000101|110010101001|110010011011|110010001101|110000111001'
        '|110000101011|110000011101|110000000001|101111110011|101111100101'
        '|101111001001|101110111011|101110101101|101110010001|101110000011'
        '|101101011001|101101001011|101100111101|101100100001|101100010011'
        '|101100000101|101001111001|101001101011|101001011101|101001000001'
        '|101000110011|101000100101|101000001001|100111111011|100111101101'
        '|100111010001|100111000011|100110011001|100110001011|100101111101'
        '|100101100001|100101010011|100101000101|100100101001|100100011011'
        '|100100001101|100010111001|100010101011|100010011101|100010000001'
        '|100001110011|100001100101|100001001001|100000111011|100000101101'
        '|100000010001|100000000011|11011111001|11011101011|11011011101'
        '|11011000001|11010110011|11010100101|11010001001|11001111011'
        '|11001101101|11001010001|11001000011|11000011001|11000001011'
        '|10111111101|10111100001|10111010011|10111000101|10110101001'
        '|10110011011|10110001101|10100111001|10100101011|10100011101'
        '|10100000001|10011110011|10011100101|10011001001|10010111011'
        '|10010101101|10010010001|10010000011|10001011001|10001001011'
        '|10000111101|10000100001|10000010011|10000000101|1101111001'
        '|1101101011|1101011101|1101000001|1100110011|1100100101|1100001001'
        '|1011111011|1011101101|1011010001|1011000011|1010011001|1010001011'
        '|1001111101|1001100001|1001010011|1001000101|1000101001|1000011011'
        '|1000001101|110111001|110101011|110011101|110000001|101110011'
        '|101100101|101001001|100111011|100101101|100010001|100000011|11011001'
        '|11001011|10111101|10100001|10010011|10000101|1101001|1011011|1001101'
        '|110001|100011|10101',
    9:
        '1111101110111|1111101100101|1111101010011|1111101000001|1111100101111'
        '|1111100011101|1111100001011|1111011100111|1111011010101'
        '|1111011000011|1111010110001|1111010011111|1111010001101'
        '|1111001010111|1111001000101|1111000110011|1111000100001'
        '|1111000001111|1110111111101|1110111101011|1110111000111'
        '|1110110110101|1110110100011|1110110010001|1110100110111'
        '|1110100100101|1110100010011|1110100000001|1110011101111'
        '|1110011011101|1110011001011|1110010100111|1110010010101'
        '|1110010000011|1110001110001|1110001011111|1110001001101'
        '|1110000010111|1110000000101|1101011110111|1101011100101'
        '|1101011010011|1101011000001|1101010101111|1101010011101'
        '|1101010001011|1101001100111|1101001010101|1101001000011'
        '|1101000110001|1101000011111|1101000001101|1100111010111'
        '|1100111000101|1100110110011|1100110100001|1100110001111'
        '|1100101111101|1100101101011|1100101000111|1100100110101'
        '|1100100100011|1100100010001|1100010110111|1100010100101'
        '|1100010010011|1100010000001|1100001101111|1100001011101'
        '|1100001001011|1100000100111|1100000010101|1100000000011'
        '|1011111110001|1011111011111|1011111001101|1011110010111'
        '|1011110000101|1011101110011|1011101100001|1011101001111'
        '|1011100111101|1011100101011|1011100000111|1011001110111'
        '|1011001100101|1011001010011|1011001000001|1011000101111'
        '|1011000011101|1011000001011|1010111100111|1010111010101'
        '|1010111000011|1010110110001|1010110011111|1010110001101'
        '|1010101010111|1010101000101|1010100110011|1010100100001'
        '|1010100001111|1010011111101|1010011101011|1010011000111'
        '|1010010110101|1010010100011|1010010010001|1010000110111'
        '|1010000100101|1010000010011|1010000000001|1000111110111'
        '|1000111100101|1000111010011|1000111000001|1000110101111'
        '|1000110011101|1000110001011|1000101100111|1000101010101'
        '|1000101000011|1000100110001|1000100011111|1000100001101'
        '|1000011010111|1000011000101|1000010110011|1000010100001'
        '|1000010001111|1000001111101|1000001101011|1000001000111'
        '|1000000110101|1000000100011|1000000010001|111110110111|111110100101'
        '|111110010011|111110000001|111101101111|111101011101|111101001011'
        '|111100100111|111100010101|111100000011|111011110001|111011011111'
        '|111011001101|111010010111|111010000101|111001110011|111001100001'
        '|111001001111|111000111101|111000101011|111000000111|110101110111'
        '|110101100101|110101010011|110101000001|110100101111|110100011101'
        '|110100001011|110011100111|110011010101|110011000011|110010110001'
        '|110010011111|110010001101|110001010111|110001000101|110000110011'
        '|110000100001|110000001111|101111111101|101111101011|101111000111'
        '|101110110101|101110100011|101110010001|101100110111|101100100101'
        '|101100010011|101100000001|101011101111|101011011101|101011001011'
        '|101010100111|101010010101|101010000011|101001110001|101001011111'
        '|101001001101|101000010111|101000000101|100011110111|100011100101'
        '|100011010011|100011000001|100010101111|100010011101|100010001011'
        '|100001100111|100001010101|100001000011|100000110001|100000011111'
        '|100000001101|11111010111|11111000101|11110110011|11110100001'
        '|11110001111|11101111101|11101101011|11101000111|11100110101'
        '|11100100011|11100010001|11010110111|11010100101|11010010011'
        '|11010000001|11001101111|11001011101|11001001011|11000100111'
        '|11000010101|11000000011|10111110001|10111011111|10111001101'
        '|10110010111|10110000101|10101110011|10101100001|10101001111'
        '|10100111101|10100101011|10100000111|10001110111|10001100101'
        '|10001010011|10001000001|10000101111|10000011101|10000001011'
        '|1111100111|1111010101|1111000011|1110110001|1110011111|1110001101'
        '|1101010111|1101000101|1100110011|1100100001|1100001111|1011111101'
        '|1011101011|1011000111|1010110101|1010100011|1010010001|1000110111'
        '|1000100101|1000010011|1000000001|111101111|111011101|111001011'
        '|110100111|110010101|110000011|101110001|101011111|101001101'
        '|100010111|100000101|11110011|11100001|11001111|10111101|10101011'
        '|10000111|1110101|1100011|1010001|111111|101101|11011',
    11:
        '1111111101101|1111111010111|1111111000001|1111110010101|1111101111111'
        '|1111101101001|1111101010011|1111100111101|1111100100111'
        '|1111100010001|1111011100101|1111011001111|1111010111001'
        '|1111010100011|1111010001101|1111000110101|1111000011111'
        '|1111000001001|1110111110011|1110111011101|1110111000111'
        '|1110110110001|1110110000101|1110101101111|1110101011001'
        '|1110101000011|1110100101101|1110100010111|1110100000001'
        '|1110011010101|1110010111111|1110010101001|1110010010011'
        '|1110001111101|1110001100111|1110001010001|1110000100101'
        '|1110000001111|1101101110101|1101101011111|1101101001001'
        '|1101100110011|1101100011101|1101100000111|1101011110001'
        '|1101011000101|1101010101111|1101010011001|1101010000011'
        '|1101001101101|1101001010111|1101001000001|1101000010101'
        '|1100111111111|1100111101001|1100111010011|1100110111101'
        '|1100110100111|1100110010001|1100101100101|1100101001111'
        '|1100100111001|1100100100011|1100100001101|1100010110101'
        '|1100010011111|1100010001001|1100001110011|1100001011101'
        '|1100001000111|1100000110001|1100000000101|1010111110101'
        '|1010111011111|1010111001001|1010110110011|1010110011101'
        '|1010110000111|1010101110001|1010101000101|1010100101111'
        '|1010100011001|1010100000011|1010011101101|1010011010111'
        '|1010011000001|1010010010101|1010001111111|1010001101001'
        '|1010001010011|1010000111101|1010000100111|1010000010001'
        '|1001111100101|1001111001111|1001110111001|1001110100011'
        '|1001110001101|1001100110101|1001100011111|1001100001001'
        '|1001011110011|1001011011101|1001011000111|1001010110001'
        '|1001010000101|1001001101111|1001001011001|1001001000011'
        '|1001000101101|1001000010111|1001000000001|1000111010101'
        '|1000110111111|1000110101001|1000110010011|1000101111101'
        '|1000101100111|1000101010001|1000100100101|1000100001111'
        '|1000001110101|1000001011111|1000001001001|1000000110011'
        '|1000000011101|1000000000111|111111110001|111111000101|111110101111'
        '|111110011001|111110000011|111101101101|111101010111|111101000001'
        '|111100010101|111011111111|111011101001|111011010011|111010111101'
        '|111010100111|111010010001|111001100101|111001001111|111000111001'
        '|111000100011|111000001101|110110110101|110110011111|110110001001'
        '|110101110011|110101011101|110101000111|110100110001|110100000101'
        '|110011101111|110011011001|110011000011|110010101101|110010010111'
        '|110010000001|110001010101|110000111111|110000101001|110000010011'
        '|101011110101|101011011111|101011001001|101010110011|101010011101'
        '|101010000111|101001110001|101001000101|101000101111|101000011001'
        '|101000000011|100111101101|100111010111|100111000001|100110010101'
        '|100101111111|100101101001|100101010011|100100111101|100100100111'
        '|100100010001|100011100101|100011001111|100010111001|100010100011'
        '|100010001101|100000110101|100000011111|100000001001|11111110011'
        '|11111011101|11111000111|11110110001|11110000101|11101101111'
        '|11101011001|11101000011|11100101101|11100010111|11100000001'
        '|11011010101|11010111111|11010101001|11010010011|11001111101'
        '|11001100111|11001010001|11000100101|11000001111|10101110101'
        '|10101011111|10101001001|10100110011|10100011101|10100000111'
        '|10011110001|10011000101|10010101111|10010011001|10010000011'
        '|10001101101|10001010111|10001000001|10000010101|1111111111'
        '|1111101001|1111010011|1110111101|1110100111|1110010001|1101100101'
        '|1101001111|1100111001|1100100011|1100001101|1010110101|1010011111'
        '|1010001001|1001110011|1001011101|1001000111|1000110001|1000000101'
        '|111101111|111011001|111000011|110101101|110010111|110000001'
        '|101010101|100111111|100101001|100010011|11111101|11100111|11010001'
        '|10100101|10001111|1111001|1100011|1001101|110111|100001',
    13:
        '1111111110001|1111111010111|1111110100011|1111110001001|1111101101111'
        '|1111101010101|1111100111011|1111100100001|1111100000111'
        '|1111011010011|1111010111001|1111010011111|1111010000101'
        '|1111001101011|1111001010001|1111000110111|1111000000011'
        '|1110111101001|1110111001111|1110110110101|1110110011011'
        '|1110110000001|1110100110011|1110100011001|1110011111111'
        '|1110011100101|1110011001011|1110010110001|1110010010111'
        '|1110001100011|1110001001001|1110000101111|1110000010101'
        '|1100111110011|1100111011001|1100110111111|1100110100101'
        '|1100110001011|1100101110001|1100101010111|1100100100011'
        '|1100100001001|1100011101111|1100011010101|1100010111011'
        '|1100010100001|1100010000111|1100001010011|1100000111001'
        '|1100000011111|1100000000101|1011111101011|1011111010001'
        '|1011110110111|1011110000011|1011101101001|1011101001111'
        '|1011100110101|1011100011011|1011100000001|1011010110011'
        '|1011010011001|1011001111111|1011001100101|1011001001011'
        '|1011000110001|1011000010111|1010111100011|1010111001001'
        '|1010110101111|1010110010101|1010101111011|1010101100001'
        '|1010101000111|1010100010011|1010011111001|1010011011111'
        '|1010011000101|1010010101011|1010010010001|1010001110111'
        '|1010001000011|1010000101001|1010000001111|1001101110011'
        '|1001101011001|1001100111111|1001100100101|1001100001011'
        '|1001011110001|1001011010111|1001010100011|1001010001001'
        '|1001001101111|1001001010101|1001000111011|1001000100001'
        '|1001000000111|1000111010011|1000110111001|1000110011111'
        '|1000110000101|1000101101011|1000101010001|1000100110111'
        '|1000100000011|1000011101001|1000011001111|1000010110101'
        '|1000010011011|1000010000001|1000000110011|1000000011001|111111111111'
        '|111111100101|111111001011|111110110001|111110010111|111101100011'
        '|111101001001|111100101111|111100010101|111011111011|111011100001'
        '|111011000111|111010010011|111001111001|111001011111|111001000101'
        '|111000101011|111000010001|110011110011|110011011001|110010111111'
        '|110010100101|110010001011|110001110001|110001010111|110000100011'
        '|110000001001|101111101111|101111010101|101110111011|101110100001'
        '|101110000111|101101010011|101100111001|101100011111|101100000101'
        '|101011101011|101011010001|101010110111|101010000011|101001101001'
        '|101001001111|101000110101|101000011011|101000000001|100110110011'
        '|100110011001|100101111111|100101100101|100101001011|100100110001'
        '|100100010111|100011100011|100011001001|100010101111|100010010101'
        '|100001111011|100001100001|100001000111|100000010011|11111111001'
        '|11111011111|11111000101|11110101011|11110010001|11101110111'
        '|11101000011|11100101001|11100001111|11001110011|11001011001'
        '|11000111111|11000100101|11000001011|10111110001|10111010111'
        '|10110100011|10110001001|10101101111|10101010101|10100111011'
        '|10100100001|10100000111|10011010011|10010111001|10010011111'
        '|10010000101|10001101011|10001010001|10000110111|10000000011'
        '|1111101001|1111001111|1110110101|1110011011|1110000001|1100110011'
        '|1100011001|1011111111|1011100101|1011001011|1010110001|1010010111'
        '|1001100011|1001001001|1000101111|1000010101|111111011|111100001'
        '|111000111|110010011|101111001|101011111|101000101|100101011'
        '|100010001|11110111|11000011|10101001|10001111|1110101|1011011'
        '|1000001|100111',
    15:
        '1110111110001|1110111010011|1110110110101|1110110010111|1110101111001'
        '|1110101011011|1110100111101|1110100000001|1110011100011'
        '|1110011000101|1110010100111|1110010001001|1110001101011'
        '|1110001001101|1110000010001|1101111110011|1101111010101'
        '|1101110110111|1101110011001|1101101111011|1101101011101'
        '|1101100100001|1101100000011|1101011100101|1101011000111'
        '|1101010101001|1101010001011|1101000110001|1101000010011'
        '|1100111110101|1100111010111|1100110111001|1100110011011'
        '|1100101111101|1100101000001|1100100100011|1100100000101'
        '|1100011100111|1100011001001|1100010101011|1100010001101'
        '|1100001010001|1100000110011|1100000010101|1011111110111'
        '|1011111011001|1011110111011|1011110011101|1011101100001'
        '|1011101000011|1011100100101|1011100000111|1011001110001'
        '|1011001010011|1011000110101|1011000010111|1010111111001'
        '|1010111011011|1010110111101|1010110000001|1010101100011'
        '|1010101000101|1010100100111|1010100001001|1010011101011'
        '|1010011001101|1010010010001|1010001110011|1010001010101'
        '|1010000110111|1010000011001|1001111111011|1001111011101'
        '|1001110100001|1001110000011|1001101100101|1001101000111'
        '|1001100101001|1001100001011|1001010110001|1001010010011'
        '|1001001110101|1001001010111|1001000111001|1001000011011'
        '|1000111111101|1000111000001|1000110100011|1000110000101'
        '|1000101100111|1000101001001|1000100101011|1000100001101'
        '|1000011010001|1000010110011|1000010010101|1000001110111'
        '|1000001011001|1000000111011|1000000011101|111011110001|111011010011'
        '|111010110101|111010010111|111001111001|111001011011|111000111101'
        '|111000000001|110111100011|110111000101|110110100111|110110001001'
        '|110101101011|110101001101|110100010001|110011110011|110011010101'
        '|110010110111|110010011001|110001111011|110001011101|110000100001'
        '|110000000011|101111100101|101111000111|101110101001|101110001011'
        '|101100110001|101100010011|101011110101|101011010111|101010111001'
        '|101010011011|101001111101|101001000001|101000100011|101000000101'
        '|100111100111|100111001001|100110101011|100110001101|100101010001'
        '|100100110011|100100010101|100011110111|100011011001|100010111011'
        '|100010011101|100001100001|100001000011|100000100101|100000000111'
        '|11101110001|11101010011|11100110101|11100010111|11011111001'
        '|11011011011|11010111101|11010000001|11001100011|11001000101'
        '|11000100111|11000001001|10111101011|10111001101|10110010001'
        '|10101110011|10101010101|10100110111|10100011001|10011111011'
        '|10011011101|10010100001|10010000011|10001100101|10001000111'
        '|10000101001|10000001011|1110110001|1110010011|1101110101|1101010111'
        '|1100111001|1100011011|1011111101|1011000001|1010100011|1010000101'
        '|1001100111|1001001001|1000101011|1000001101|111010001|110110011'
        '|110010101|101110111|101011001|100111011|100011101|11100001|11000011'
        '|10100101|10000111|1101001|1001011|101101',
    17:
        '1111111001111|1111110101101|1111110001011|1111101101001|1111101000111'
        '|1111100100101|1111100000011|1111011100001|1111010111111'
        '|1111010011101|1111001111011|1111001011001|1111000110111'
        '|1111000010101|1110110101111|1110110001101|1110101101011'
        '|1110101001001|1110100100111|1110100000101|1110011100011'
        '|1110011000001|1110010011111|1110001111101|1110001011011'
        '|1110000111001|1110000010111|1101111110101|1101111010011'
        '|1101110001111|1101101101101|1101101001011|1101100101001'
        '|1101100000111|1101011100101|1101011000011|1101010100001'
        '|1101001111111|1101001011101|1101000111011|1101000011001'
        '|1100101101111|1100101001101|1100100101011|1100100001001'
        '|1100011100111|1100011000101|1100010100011|1100010000001'
        '|1100001011111|1100000111101|1100000011011|1011111111001'
        '|1011111010111|1011110110101|1011110010011|1011101001111'
        '|1011100101101|1011100001011|1011011101001|1011011000111'
        '|1011010100101|1011010000011|1011001100001|1011000111111'
        '|1011000011101|1010111111011|1010111011001|1010110110111'
        '|1010110010101|1010100101111|1010100001101|1010011101011'
        '|1010011001001|1010010100111|1010010000101|1010001100011'
        '|1010001000001|1010000011111|1001111111101|1001111011011'
        '|1001110111001|1001110010111|1001101110101|1001101010011'
        '|1001100001111|1001011101101|1001011001011|1001010101001'
        '|1001010000111|1001001100101|1001001000011|1001000100001'
        '|1000011101111|1000011001101|1000010101011|1000010001001'
        '|1000001100111|1000001000101|1000000100011|1000000000001|111111011111'
        '|111110111101|111110011011|111101111001|111101010111|111100110101'
        '|111100010011|111011001111|111010101101|111010001011|111001101001'
        '|111001000111|111000100101|111000000011|110111100001|110110111111'
        '|110110011101|110101111011|110101011001|110100110111|110100010101'
        '|110010101111|110010001101|110001101011|110001001001|110000100111'
        '|110000000101|101111100011|101111000001|101110011111|101101111101'
        '|101101011011|101100111001|101100010111|101011110101|101011010011'
        '|101010001111|101001101101|101001001011|101000101001|101000000111'
        '|100111100101|100111000011|100110100001|100101111111|100101011101'
        '|100100111011|100100011001|100001101111|100001001101|100000101011'
        '|100000001001|11111100111|11111000101|11110100011|11110000001'
        '|11101011111|11100111101|11100011011|11011111001|11011010111'
        '|11010110101|11010010011|11001001111|11000101101|11000001011'
        '|10111101001|10111000111|10110100101|10110000011|10101100001'
        '|10100111111|10100011101|10011111011|10011011001|10010110111'
        '|10010010101|10000101111|10000001101|1111101011|1111001001|1110100111'
        '|1110000101|1101100011|1101000001|1100011111|1011111101|1011011011'
        '|1010111001|1010010111|1001110101|1001010011|1000001111|111101101'
        '|111001011|110101001|110000111|101100101|101000011|100100001|11111111'
        '|11011101|10111011|10011001|1110111|1010101|110011'}


def _kata_3(d: int = 90) -> str:
    if not d:
        return ''
    sub = _kata_3(d - 1)
    if sub:
        return (
            f'(11'
            f'|10{ sub }01'
            f'|01{ sub }10'
            f'|0{ sub }'
            f'|{ sub })+'
        )
    return (
        f'(11'
        f'|10{ sub }01'
        f'|01{ sub }10'
        f'|0{ sub })+'
    )


@lru_cache()
def _kata(n: int) -> str:
    if n % 2 == 0:
        return f'{ _kata(n // 2) }0'
    if n == 3:
        return _kata_3()
    return f'(0|{ bin(n)[2:] }|{ SOLUTION_ODD[n] })+'


# 01?:*+^$()[]|
@lru_cache()
def kata(n: int) -> str:
    """
    Kata.
    """
    return f'^0*(0|({ _kata(n) }))$'


def _main(src: str) -> Iterable[str]:
    for j in range(LIMIT):
        sample = bin(j)[2:]
        for i in range(1, 19):
            match = search(kata(i), sample)
            if j % i == 0:
                if not match:
                    SOLUTION_ODD[i] = '|'.join((sample, SOLUTION_ODD[i]))
                    match = search(kata(i), sample)
                assert match, (i, j, bin(j))
            else:
                assert not match, (i, j)

    start, mid = split('LIMIT' r' = \d+', src)

    yield start
    yield 'LIMIT' ' = '
    yield str(LIMIT << 1)

    mid, end = split('SOLUTION_ODD' r' = {[^}]+?}', mid)

    yield mid
    yield 'SOLUTION_ODD' ' = {\n'
    yield ' ' * 4
    yield '1: \''
    yield SOLUTION_ODD.pop(1)
    yield '\''

    for k, v in SOLUTION_ODD.items():
        it = iter(v.split('|'))
        first = next(it)

        yield ',\n'
        yield ' ' * 4
        yield str(k)
        yield ':\n'
        yield ' ' * 8
        yield '\''
        yield first

        line_length = 9 + len(first)
        for bits in map('|{}'.format, it):
            line_length += len(bits)
            if line_length >= 79:
                yield '\'\n'
                yield ' ' * 8
                yield '\''
                line_length = 9 + len(bits)
            yield bits
        yield '\''

    yield '}'
    yield end


def main() -> None:
    """
    Main.
    """
    with open(__file__) as istream:
        src = istream.read()
    with open(__file__, 'w') as ostream:
        ostream.writelines(_main(src))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
