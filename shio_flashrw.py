import argparse
from pynrfjprog import API

# Default settings
JLINK_SPEED_KHZ = 4000
DEFAULT_START_ADDR = "0x60000"
DEFAULT_LENGTH = "0x40000"
DEFAULT_FILE_NAME = "shio_flashrw.bin"
DEFAULT_FILE_NAME_HEX = "shio_flashrw.hex"

def convert(str):
    if str.upper().startswith("0X"):
        return int(str, 16)
    else:
        return int(str)

if __name__ == '__main__':
    # Print banner
    print("JLink Flash read/write")

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("read", "write"), nargs="?", default="read")
    parser.add_argument("--start", type=str, nargs="?", default=DEFAULT_START_ADDR)
    parser.add_argument("--length", type=str, nargs="?", default=DEFAULT_LENGTH)
    parser.add_argument("--file", type=str, nargs="?", default=DEFAULT_FILE_NAME)
    args = parser.parse_args()

    # Open connection to jlink
    nrfjprog = API.API('NRF52')
    nrfjprog.open()
    try:
        nrfjprog.connect_to_emu_without_snr(jlink_speed_khz=JLINK_SPEED_KHZ)
    except:
        print("No jlink detected!")
        exit()

    # Perform action
    if args.action == "read":
        # Read flash
        bin_data = nrfjprog.read(addr=convert(args.start), data_len=convert(args.length))
        # Write to file
        fh = open(args.file, "wb")
        fh.write(bytearray(bin_data))            
        fh.close()
        
        # Open in binary mode (so you don't read two byte line endings on Windows as one byte)
        # and use with statement (always do this to avoid leaked file descriptors, unflushed files)
        with open(args.file, 'rb') as f:
            # Slurp the whole file and efficiently convert it to hex all at once
            s = f.read().hex()
            split = " ".join(s[i:i+2] for i in range(0, len(s), 2))
            hexdata = bytes(split, encoding = 'utf8')
        fb = open(DEFAULT_FILE_NAME_HEX, "wb")
        fb.write(bytearray(hexdata))
        fb.close()
    else:
        # Read file
        fh = open(args.file, "rb")
        bin_data = bytearray(fh.read())
        fh.close()
        # Write flash
        if convert(args.length) == len(bin_data):
            nrfjprog.write(addr=convert(args.start), data=bin_data, control=True)
        else:
            print("Number of bytes miss-match!")

    # Cleanup
    nrfjprog.close()
