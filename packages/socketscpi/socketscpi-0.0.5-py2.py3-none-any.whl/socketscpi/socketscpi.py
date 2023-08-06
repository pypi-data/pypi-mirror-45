"""
socketscpi
Author: Morgan Allison, Keysight RF/uW Application Engineer
This program provides a socket interface to Keysight test equipment.
It handles sending commands, receiving query results, and
reading/writing binary block data.
"""

import socket
import numpy as np


class SocketInstrument:
    def __init__(self, host, port=5025, timeout=10, noDelay=True):
        """Open socket connection with settings for instrument control."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if noDelay:
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.setblocking(False)
        self.socket.settimeout(timeout)
        self.socket.connect((host, port))

        self.instId = self.query('*idn?')

    def disconnect(self):
        """Gracefully close connection."""
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def query(self, cmd):
        """Sends query to instrument and returns reply as string."""
        # self.write(cmd)

        msg = '{}\n'.format(cmd)
        self.socket.send(msg.encode('latin_1'))

        # Read continuously until termination character is found.
        response = b''
        while response[-1:] != b'\n':
            response += self.socket.recv(1024)

        # Strip out whitespace and return.
        return response.decode('latin_1').strip()

    def write(self, cmd):
        """Write a command string to instrument."""
        msg = '{}\n'.format(cmd)
        self.socket.send(msg.encode('latin_1'))
        # msg = '{}\n*esr?'.format(cmd)
        # ret = self.query(msg)
        # if (int(ret) != 0):
        #     raise SockInstError('esr non-zero: {}'.format(ret))

    def err_check(self):
        """Prints out all errors and clears error queue.

        Certain instruments format the syst:err? response differently, so remove whitespace and
        extra characters before checking."""
        err = []
        if 'mso' in self.instId.lower() or 'dso' in self.instId.lower():
            cmd = 'SYST:ERR? string'
        else:
            cmd = 'SYST:ERR?'
        temp = self.query(cmd).strip().replace('+', '').replace('-', '')
        while temp != '0,"No error"':
            err.append(temp)
            temp = self.query('syst:err?').strip().replace('+', '').replace('-', '')
        if err:
            raise SockInstError(err)

    def binblockread(self, cmd, datatype='b', debug=False):
        """Send a command and read data with IEEE 488.2 binary block format

        cmd: string containing SCPI command
        datatype: data type specified using the same naming convention used
            by Python's built-in struct module
            https://docs.python.org/3/library/struct.html#format-characters

        The waveform is formatted as:
        #<x><yyy><data><newline>, where:
        <x> is the number of y bytes. For example, if <yyy>=500, then <x>=3.
        NOTE: <x> is a hexadecimal number.
        <yyy> is the number of bytes to transfer. Care must be taken
        when selecting the data type used to interpret the data.
        The dtype argument used to read the data must match the data
        type used by the instrument that sends the data.
        <data> is the data payload in binary format.
        <newline> is a single byte new line character at the end of the data.
        """

        # Decode data type
        if datatype == 'b':
            dtype = np.int8
        elif datatype == 'B':
            dtype = np.uint8
        elif datatype == 'h':
            dtype = np.int16
        elif datatype == 'H':
            dtype = np.uint16
        elif datatype == 'i' or datatype == 'l':
            dtype = np.int32
        elif datatype == 'I' or datatype == 'L':
            dtype = np.uint32
        elif datatype == 'q':
            dtype = np.int64
        elif datatype == 'Q':
            dtype = np.uint64
        elif datatype == 'f':
            dtype = np.float32
        elif datatype == 'd':
            dtype = np.float64
        else:
            raise BinblockError('Invalid data type selected.')

        # Send command/query
        self.write(cmd)

        # Read # character, raise exception if not present.
        if self.socket.recv(1) != b'#':
            raise BinblockError('Data in buffer is not in binblock format.')

        # Extract header length and number of bytes in binblock.
        headerLength = int(self.socket.recv(1).decode('latin_1'), 16)
        numBytes = int(self.socket.recv(headerLength).decode('latin_1'))

        if debug:
            print('Header: #{}{}'.format(headerLength, numBytes))

        rawData = bytearray(numBytes)
        buf = memoryview(rawData)

        # While there is data left to read...
        while numBytes:
            # Read data from instrument into buffer.
            bytesRecv = self.socket.recv_into(buf, numBytes)
            # Slice buffer to preserve data already written to it.
            buf = buf[bytesRecv:]
            # Subtract bytes received from total bytes.
            numBytes -= bytesRecv
            if debug:
                print('numBytes: {}, bytesRecv: {}'.format(
                    numBytes, bytesRecv))

        # Receive termination character.
        term = self.socket.recv(1)
        if debug:
            print('Term char: ', term)
        # If term char is incorrect or not present, raise exception.
        if term != b'\n':
            print('Term char: {}, rawData Length: {}'.format(
                term, len(rawData)))
            raise BinblockError('Data not terminated correctly.')

        # Convert binary data to NumPy array of specified data type and return.
        return np.frombuffer(rawData, dtype=dtype)

    # noinspection PyUnresolvedReferences
    @staticmethod
    def binblock_header(data):
        """Returns a IEEE 488.2 binary block header

        #<x><yyy>..., where:
        <x> is the number of y bytes. For example, if <yyy>=500, then <x>=3.
        NOTE: <x> is a hexadecimal number.
        <yyy> is the number of bytes to transfer. """

        numBytes = memoryview(data).nbytes
        return f'#{len(str(numBytes))}{numBytes}'

    def binblockwrite(self, cmd, data, debug=False, esr=True):
        """Send data with IEEE 488.2 binary block format

        The data is formatted as:
        #<x><yyy><data><newline>, where:
        <x> is the number of y bytes. For example, if <yyy>=500, then <x>=3.
        NOTE: <x> is a hexadecimal number.
        <yyy> is the number of bytes to transfer.
        <data> is the data payload in binary format.
        <newline> is a single byte new line character at the end of the data.
        """

        header = self.binblock_header(data)

        # Send message, header, data, and termination
        self.socket.send(cmd.encode('latin_1'))
        self.socket.send(header.encode('latin_1'))
        self.socket.send(data)
        self.socket.send(b'\n')

        if debug:
            print(f'binblockwrite --')
            print(f'msg: {cmd}')
            print(f'header: {header}')

        # Check error status register and notify of problems
        if esr:
            r = self.query('*esr?')
            if int(r) is not 0:
                self.err_check()


class SockInstError(Exception):
    pass


class BinblockError(Exception):
    pass
