import wmi
import os
import threading

m_wmi = wmi.WMI()

def showAdapters():
    m_NAC = m_wmi.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    print("-------------Adapter Informations---------------\n")
    for obj in m_NAC:
        print("{:5s}{:20s}{:5s}".format("", "Adapter Index", ""),
              obj.Index)
        print("{:5s}{:20s}{:5s}".format("", "Adapter SettingID", ""),
              obj.SettingID)
        print("{:5s}{:20s}{:5s}".format("", "Description", ""),
              obj.Description.encode("cp936"))
        print("{:5s}{:20s}{:5s}".format("", "IPAdress", ""),
              obj.IPAddress)
        print("{:5s}{:20s}{:5s}".format("", "IPSubnet", ""),
              obj.IPSubnet)
        print("{:5s}{:20s}{:5s}".format("", "Default_GW", ""),
              obj.DefaultIPGateway)
        print("{:5s}{:20s}{:5s}".format("", "DNS", ""),
              obj.DNSServerSearchOrder)

    print("-----------------------------------------------\n")

    return len(m_NAC), m_NAC

def changeIP(obj, ip, subnetMask, gw):
    returnValue1 = obj.EnableStatic(
        IPAddress=ip, SubnetMask=subnetMask
        )
    returnValue2 = obj.SetGateways(
        DefaultIPGateway=gw,
        GatewayCostMetric= [1]
        )
    print(returnValue1)
    return returnValue1 and returnValue2

def ping_ip(ip):
    cmd = ['ping', '-n', '1', ip]
    out = os.popen(' '.join(cmd)).readlines()
    #print(ip)
    flag = False
    for line in list(out):
        if not line:
            continue
        if str(line).upper().find("TTL")>=0:
            flag = True
            break
    if flag:
        print("[+] ip {:15s} is active".format(ip))
    

    return flag

def scanNetwork(subnet):
    ip_list = list()
    print("--------------Current subnet is {:s}.0".format(subnet))
    for i in range(1, 255):
        ip = "{:s}.{:s}".format(subnet, str(i))
        return_value = ping_ip(ip)
        if return_value:
            ip_list.append(ip)
    return ip_list

def main():
    l, m = showAdapters()
    t = 1
    act_ip = list()
    if l > 1:
        t = int(
            input('There are more than 1 adapter, input index to chose one'))

    print("------Network scanning")
    for i in range(0, 255):
        subnet = "192.168.{:s}".format(str(i))
        ip = ["192.168.{:s}.254".format(str(i))]
        subnetMask = ["255.255.255.0"]
        gw = ["192.168.{:s}.1".format(str(i))]
        changeIP(m[t-1], ip, subnetMask, gw)
        act_ip.append(scanNetwork(subnet))

if __name__ == '__main__':
    main()
    #l, m = showAdapters()
    #ip = ['192.168.0.255']
    #subnetMask = ['255.255.255.0']
    #gw = ['192.168.0.1']
    #changeIP(m[0], ['192.168.0.254'], ['255.255.255.0'], ['192.168.1.0'])
    
#l, m = showAdapters()
#changeIP(m[0], ['192.168.1.1'], ['255.255.255.0'], ['192.168.1.0'])
