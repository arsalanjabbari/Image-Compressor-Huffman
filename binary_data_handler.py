import os

def read_image_bit_string(image_path):
    bit_string = ""
    with open(image_path, 'rb') as image:
        byte = image.read(1)
        while byte:
            byte_value = ord(byte)
            bits = bin(byte_value)[2:].rjust(8, '0')
            bit_string += bits
            byte = image.read(1)
    return bit_string


def save_data(bit_string_or_dictionary, save_path, data_type):
    # Create the directory if it doesn't exist
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if data_type == 'image':
        with open(save_path, 'wb') as file:
            for i in range(0, len(bit_string_or_dictionary), 8):
                byte_bits = bit_string_or_dictionary[i:i + 8]
                file.write(bytes([int(byte_bits, 2)]))
    elif data_type == 'dictionary':
        with open(save_path, 'w') as file:
            for key, value in bit_string_or_dictionary.items():
                file.write('%s:%s\n' % (key, value))
    else:
        raise ValueError("Invalid data_type. Supported values: 'image', 'dictionary'")

