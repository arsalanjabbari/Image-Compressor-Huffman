import heapq
import binary_data_handler


# Define the Node class for the Huffman tree
class Node:

    def __init__(self, frequency, symbol, left=None, right=None):
        self.frequency = frequency
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huffman_direction = ''  # Direction in the Huffman tree

    def __lt__(self, nxt):
        return self.frequency < nxt.frequency


huffman_codes = {}  # Dictionary to store Huffman codes


# Compress image_bit_string using Huffman codes
def get_compressed_image(image_bit_string):
    compressed_image_bit_string = ""

    # Process the image bit string in chunks of 8 bits
    for i in range(0, len(image_bit_string), 8):
        byte = image_bit_string[i:i + 8]
        compressed_image_bit_string += huffman_codes[byte]  # Append Huffman code

    return compressed_image_bit_string


# Recursively calculate Huffman codes for each symbol
def calculate_huffman_codes(node, code=''):
    code += node.huffman_direction  # Append the Huffman direction

    if node.left:
        calculate_huffman_codes(node.left, code)  # Traverse left
    if node.right:
        calculate_huffman_codes(node.right, code)  # Traverse right

    if not node.left and not node.right:
        huffman_codes[node.symbol] = code  # Assign Huffman code to symbol


# Build the merged Huffman tree from byte frequencies
def get_merged_huffman_tree(byte_to_frequency):
    huffman_tree = [Node(frequency, byte) for byte, frequency in byte_to_frequency.items()]
    heapq.heapify(huffman_tree)  # Convert list to a min-heap

    # Merge nodes to construct the Huffman tree
    while len(huffman_tree) > 1:
        left = heapq.heappop(huffman_tree)
        right = heapq.heappop(huffman_tree)

        left.huffman_direction = "0"
        right.huffman_direction = "1"

        merged_node = Node(left.frequency + right.frequency,
                           left.symbol + right.symbol, left, right)

        heapq.heappush(huffman_tree, merged_node)  # Push merged node back

    return huffman_tree[0]  # Return the root of the Huffman tree


# Calculate byte frequencies from the image bit string
def get_frequency(image_bit_string):
    byte_to_frequency = {}

    # Process the image bit string in chunks of 8 bits
    for i in range(0, len(image_bit_string), 8):
        byte = image_bit_string[i:i + 8]
        byte_to_frequency[byte] = byte_to_frequency.get(byte, 0) + 1  # Increment frequency

    return byte_to_frequency


# Compress the image bit string using Huffman coding
def compress(image_bit_string):
    byte_to_frequency = get_frequency(image_bit_string)
    merged_huffman_tree = get_merged_huffman_tree(byte_to_frequency)
    calculate_huffman_codes(merged_huffman_tree)

    # Write Huffman codes to a file
    binary_data_handler.save_data(huffman_codes, "./IO/Outputs/huffman_codes.txt", 'dictionary')

    return get_compressed_image(image_bit_string)


# Decompress the compressed image bit string
def decompress(compressed_image_bit_string):
    decompressed_image_bit_string = ""
    current_code = ""
    code_to_byte = {code: byte for byte, code in huffman_codes.items()}

    # Iterate through the compressed bit string
    for bit in compressed_image_bit_string:
        current_code += bit

        # Check if the current code corresponds to a byte
        if current_code in code_to_byte:
            decompressed_image_bit_string += code_to_byte[current_code]
            current_code = ""  # Reset the code buffer

    return decompressed_image_bit_string
