#
# This class is automatically generated by mig. DO NOT EDIT THIS FILE.
# This class implements a Python interface to the 'BootMsg'
# message type.
#

import tinyos.message.Message

# The default size of this message type in bytes.
DEFAULT_MESSAGE_SIZE = 14

# The Active Message type associated with this message.
AM_TYPE = 8

class BootMsg(tinyos.message.Message.Message):
    # Create a new BootMsg of size 14.
    def __init__(self, data="", addr=None, gid=None, base_offset=0, data_length=14):
        tinyos.message.Message.Message.__init__(self, data, addr, gid, base_offset, data_length)
        self.amTypeSet(AM_TYPE)
    
    # Get AM_TYPE
    def get_amType(cls):
        return AM_TYPE
    
    get_amType = classmethod(get_amType)
    
    #
    # Return a String representation of this message. Includes the
    # message type name and the non-indexed field values.
    #
    def __str__(self):
        s = "Message <BootMsg> \n"
        try:
            s += "  [version=";
            for i in range(0, 14):
                s += "0x%x " % (self.getElement_version(i) & 0xff)
            s += "]\n";
        except:
            pass
        return s

    # Message-type-specific access methods appear below.

    #
    # Accessor methods for field: version
    #   Field type: short[]
    #   Offset (bits): 0
    #   Size of each element (bits): 8
    #

    #
    # Return whether the field 'version' is signed (False).
    #
    def isSigned_version(self):
        return False
    
    #
    # Return whether the field 'version' is an array (True).
    #
    def isArray_version(self):
        return True
    
    #
    # Return the offset (in bytes) of the field 'version'
    #
    def offset_version(self, index1):
        offset = 0
        if index1 < 0 or index1 >= 14:
            raise IndexError
        offset += 0 + index1 * 8
        return (offset / 8)
    
    #
    # Return the offset (in bits) of the field 'version'
    #
    def offsetBits_version(self, index1):
        offset = 0
        if index1 < 0 or index1 >= 14:
            raise IndexError
        offset += 0 + index1 * 8
        return offset
    
    #
    # Return the entire array 'version' as a short[]
    #
    def get_version(self):
        tmp = [None]*14
        for index0 in range (0, self.numElements_version(0)):
                tmp[index0] = self.getElement_version(index0)
        return tmp
    
    #
    # Set the contents of the array 'version' from the given short[]
    #
    def set_version(self, value):
        for index0 in range(0, len(value)):
            self.setElement_version(index0, value[index0])

    #
    # Return an element (as a short) of the array 'version'
    #
    def getElement_version(self, index1):
        return self.getUIntElement(self.offsetBits_version(index1), 8, 1)
    
    #
    # Set an element of the array 'version'
    #
    def setElement_version(self, index1, value):
        self.setUIntElement(self.offsetBits_version(index1), 8, value, 1)
    
    #
    # Return the total size, in bytes, of the array 'version'
    #
    def totalSize_version(self):
        return (112 / 8)
    
    #
    # Return the total size, in bits, of the array 'version'
    #
    def totalSizeBits_version(self):
        return 112
    
    #
    # Return the size, in bytes, of each element of the array 'version'
    #
    def elementSize_version(self):
        return (8 / 8)
    
    #
    # Return the size, in bits, of each element of the array 'version'
    #
    def elementSizeBits_version(self):
        return 8
    
    #
    # Return the number of dimensions in the array 'version'
    #
    def numDimensions_version(self):
        return 1
    
    #
    # Return the number of elements in the array 'version'
    #
    def numElements_version():
        return 14
    
    #
    # Return the number of elements in the array 'version'
    # for the given dimension.
    #
    def numElements_version(self, dimension):
        array_dims = [ 14,  ]
        if dimension < 0 or dimension >= 1:
            raise IndexException
        if array_dims[dimension] == 0:
            raise IndexError
        return array_dims[dimension]
    
    #
    # Fill in the array 'version' with a String
    #
    def setString_version(self, s):
         l = len(s)
         for i in range(0, l):
             self.setElement_version(i, ord(s[i]));
         self.setElement_version(l, 0) #null terminate
    
    #
    # Read the array 'version' as a String
    #
    def getString_version(self):
        carr = "";
        for i in range(0, 4000):
            if self.getElement_version(i) == chr(0):
                break
            carr += self.getElement_version(i)
        return carr
    
