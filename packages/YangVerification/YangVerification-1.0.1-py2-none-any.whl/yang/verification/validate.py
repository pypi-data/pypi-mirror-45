# coding=utf-8
import vlan_schema
import vlan_ip_schema
import vlan_update_schema
import pyangbind.lib.pybindJSON as pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder
import json
import traceback
from pyangbind.lib.xpathhelper import YANGPathHelper
import vlan_validate
import bgp_network_validate
import portChannel_validate


def start_check(type, action, target, hostname, options=None):
    msg = "ok"
    module = type + "_check"
    msg = globals().get(module)(action, target, hostname)
    return msg


def vlan_check(action, target, hostname):

    if action == "add":
        ## 如果是增则对 先检查整体添加完后是否符合yang model 然后对所有相关的key进行逐一增加检查
        msg = vlan_validate.check_add_vlan_ip(target, hostname)
        return msg


    if action == "new":
        try:
            adminStatus = target.get("adminStatus", "")
            if not adminStatus == "up":
                return "配置文件校验未通过,新建vlan，adminstatus 必须为up"
            return vlan_validate.check_new_vlan(target, hostname)

        except Exception, e:
            return "配置未通过yang model检测:" + e.message


    if action == "update":
        try:
            msg = vlan_validate.check_update_vlan(target, hostname)
            return msg
        except Exception, e:
            return "配置未通过yang model监测:"+ e.message

    if action == "remove":
        try:
            msg = vlan_validate.check_vlan_remove_ip(target, hostname)
            return msg
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测:" + e.message


def portChannel_check(action, target, hostname):
    if action == "add":
        try:
        ## 如果是增则对 先检查整体添加完后是否符合yang model 然后对所有相关的key进行逐一增加检查
            msg = portChannel_validate.check_add_vlan(target, hostname)
            return msg
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测:" + e.message


    if action == "remove":
        try:
            msg = portChannel_validate.check_remove_vlan(target, hostname)
            return msg
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测:" + e.message

def bgp_network_check(action, target, hostname):
    if action == "add":
        try:
            ## 如果是增则对 先检查整体添加完后是否符合yang model 然后对所有相关的key进行逐一增加检查
            msg = bgp_network_validate.check_bgp_network_add_ip(target, hostname)
            return msg
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测:" + e.message

    if action == "remove":
        try:
            msg = bgp_network_validate.check_bgp_network_remove_ip(target, hostname)
            return msg
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测:" + e.message




if __name__ == "__main__":
    target = {
        "VLAN10": {
            "ipv4Address": ["11.210.88.1/30", "192.168.0.1/30"],
            "ipv6Address": ["fe00::4/64", "fe00::3/64"]
        }
    }

    current = {"VLAN": {
        "VLAN10": {
            "ipv4Address": ["11.210.88.1/30", "192.168.0.1/30"],
            "ipv6Address": ["fe00::4/64", "fe00::3/64"]
        }
    }
    }
    # msg = check_new_vlan(target, current)
    msg = start_check("vlan", "new", target, "11.161.62.23")
    print msg
