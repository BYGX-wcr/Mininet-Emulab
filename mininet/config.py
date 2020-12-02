class Subnet:
    def __init__(self, ipStr=None, prefixLen=None):
        self.prefixLen = prefixLen
        self.ipStr = self.extractPrefix(ipStr, prefixLen)
        self.ip = Subnet.strToIp(self.ipStr)
        self.ptr = 0 if prefixLen == 32 else 1
        self.limit = pow(2, 32 - prefixLen)
        self.bitmap = [0] * self.limit

        if self.prefixLen is None or self.ipStr is None:
            print("Configuration is invalid, prefixLen: %s, ipStr: %s" % (prefixLen, ipStr))
    
    def allocateIPAddr(self):
        """
        Allocate an ip address automatically(with netmask)
        """
        if self.ptr >= self.limit:
            print("Subnet %s/%d has run out of address space!" % {self.ipStr, self.prefixLen})
            return None

        # search for an available address
        while self.bitmap[self.ptr]:
            self.ptr += 1
        # compute the new ip and update bitmap & pointer
        newIp = self.ip + self.ptr
        self.bitmap[self.ptr] = True
        self.ptr = self.ptr + 1

        return Subnet.ipToStr(newIp) + '/' + str(self.prefixLen)
    
    def assignIpAddr(self, ipStr):
        """
        Assign a certain ip address designated by arg:ipStr.
        Return the ip address with netmask if the operation succeeds, none otherwise.
        """
        if self.ipStr != Subnet.extractPrefix(ipStr, self.prefixLen):
            print("Mismatched IP prefix!")
            return None
        
        segmentIndex = Subnet.strToIp(ipStr) - self.ip
        if self.bitmap[segmentIndex]:
            print("The IP address has been allocated")
            return None
        else:
            self.bitmap[segmentIndex] = True
            return ipStr + "/" + str(self.prefixLen)

    def getNetworkPrefix(self):
        return self.ipStr + "/" + str(self.prefixLen)

    @staticmethod
    def extractPrefix(ipStr, prefixLen):
        """
        Extract the prefix of the arg:ipStr based on arg:prefixLen
        """
        # transform the str into subnet prefix
        ip = Subnet.strToIp(ipStr)
        ip = (ip >> (32 - prefixLen)) << (32 - prefixLen)

        # transform the subnet prefix into str
        return Subnet.ipToStr(ip)

    @staticmethod
    def strToIp(ipStr):
        """
        Transform ip string into ip integer
        """
        segments = str(ipStr).split('.')
        nums = [int(i) for i in segments]
        ip = nums[0] * pow(2, 24) + nums[1] * pow(2, 16) + nums[2] * pow(2, 8) + nums[3]
        return ip

    @staticmethod
    def ipToStr(ip):
        """
        Transform ip integer into ip string
        """
        nums = [0] * 4
        for i in range(4):
            nums[i] = ((ip << (i * 8) & 0xffffffff) >> 24)

        return "%d.%d.%d.%d" % (nums[0], nums[1], nums[2], nums[3])

# used for test
if __name__ == "__main__":
    snet = Subnet(ipStr="10.1.0.0", prefixLen=24)
    a = snet.allocateIPAddr()
    b = snet.allocateIPAddr()
    print(a)
    print(b)