import huaweisms.api.user
import huaweisms.api.wlan
import huaweisms.api.sms
import huaweisms.api.device

ctx = huaweisms.api.user.quick_login("admin", "start1119", modem_host='192.168.8.1')
print(ctx)
# output: <ApiCtx modem_host=192.168.8.1>

# sending sms
information = huaweisms.api.device.information(ctx)  #.device.reboot)
basic_information = huaweisms.api.device.basic_information(ctx)  #.device.reboot)
print(information)
basic_information = huaweisms.api.device.reboot(ctx)  #.device.reboot)
#.sms.send_sms(
#    ctx,
#    '9920171292',
#    'this is the sms message'
#)

# connected devices
device_list = huaweisms.api.wlan.get_connected_hosts(ctx)

