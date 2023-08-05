# coding=utf-8
from pyangbind.lib.xpathhelper import YANGPathHelper
import pyangbind.lib.pybindJSON as pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder
import traceback
import json
import vlan_schema
import vlan_ip_schema
import vlan_update_schema
from common import get_current_config




def get_current_vlan(current_config):
    ### 这里预留获取逻辑 直接在task上实现或者如果校验是个模板的话则调用get模板来实现
    ### 暂时只能用北向api来实现
    ph = YANGPathHelper()

    try:
        result = {
            "VLAN":current_config.get("VLAN")
        }
        current_vlan = pybindJSON.loads(result, vlan_schema, "vlan_schema", path_helper=ph)
    except Exception,e:
        raise Exception("设备上vlan配置未通过yang model 校验"+ e.message)
    return current_vlan

def check_add_vlan_ip(target, hostname):
    ## 新增只允许新增ipAddress

    ph = YANGPathHelper()
    try:
        current_config = get_current_config(hostname)

        ## 返回的是一个Json对象
        current_vlan = get_current_vlan(current_config)

    except Exception, e:
        print traceback.format_exc(e)
        return e.message

    try:
        vlan_ip_target = {
            "VLAN_IP": target
        }
        additional = pybindJSON.loads(vlan_ip_target, vlan_ip_schema, "vlan_ip_schema", path_helper=ph)
    except Exception, e:
        print traceback.format_exc(e)
        return "配置未通过yang model检测:" + e.message


    current = json.loads(pybindJSON.dumps(current_vlan))
    ip_types = ["ipv4Address", "ipv6Address"]
    try:
        addtional = target["VLAN_IP"]
        base = current["VLAN"]
        for k in addtional.keys():
            vlan_base_ipAddress = base[k]["ipAddress"]
            addtional_ipAddress = addtional[k]["ipAddress"]
            for ip_type in ip_types:
                if addtional_ipAddress.get(ip_type, []) and vlan_base_ipAddress.get(ip_type, []):
                    for ip in addtional_ipAddress[ip_type]:
                        if ip in vlan_base_ipAddress[ip_type]:
                            return "存在重复ip" + ip
                    vlan_base_ipAddress[ip_type].extend(addtional_ipAddress[ip_type])
                elif not addtional_ipAddress.get(ip_type, []):
                    continue
                else:
                    vlan_base_ipAddress[ip_type] = addtional_ipAddress[ip_type]

        print current
        pybindJSON.loads(current, vlan_schema, "vlan_schema", path_helper=YANGPathHelper())
        return "ok"
    except Exception, e:
        print traceback.format_exc(e)
        return "yang model转换失败,请检查配置"




def check_new_vlan(target, hostname):
    ph = YANGPathHelper()
    try:
        current_config = get_current_config(hostname)

        ## 返回的是一个Json对象
        current_vlan = get_current_vlan(current_config)
    except Exception, e:
        return e.message

    current = json.loads(pybindJSON.dumps(current_vlan))
    try:
        current_vlans = current.get("VLAN")
        for vlan in target.keys():
            if current_vlans.has_key(vlan):
                return "配置中新建vlan和交换机上已有vlan重复"

        merge_dict = current["VLAN"].update(current)
        after = pybindJSON.loads(merge_dict, vlan_schema, "vlan_schema", path_helper=ph)
        print pybindJSON.dumps(after)
        return "ok"
    except Exception, e:
        print traceback.format_exc(e)
        return "新增配置后yang model检查失败" + e.message

def check_vlan_remove_ip(target, hostanme):
    ph = YANGPathHelper()
    try:
        vlan_ip_target = {
            "VLAN_IP": target
        }
        additional = pybindJSON.loads(vlan_ip_target, vlan_ip_schema, "vlan_ip_schema", path_helper=ph)
    except Exception, e:
        print traceback.format_exc(e)
        return "配置未通过yang model检测:" + e.message

    return "ok"

def check_update_vlan(target, hostname):
    try:
        vlan_target = {
            "VLAN": target
        }
        additional = pybindJSON.loads(vlan_target, vlan_update_schema, "vlan_update_schema", path_helper=ph)
    except Exception, e:
        return "配置未通过yang model监测:" + e.message
    return "ok"



