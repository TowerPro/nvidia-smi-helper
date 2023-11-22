
from flask import Flask, jsonify, render_template, g
from update_cuda_api import update_cuda_device_info
import orjson
import os
from globals import set_switch_status, get_switch_status
import time

app = Flask(__name__)



@app.route('/')
def index():
    json = {}
    update_cuda_device_info(json)
    # json_str = orjson.dumps(json).decode()
    otp = "online GPU / total GPU: {}/{}".format(
        json['online_cnt'], json['device_cnt'])

    dev0 = eval(json['device_idx_0'])
    dev1 = eval(json['device_idx_1'])
    dev2 = eval(json['device_idx_2'])
    dev3 = eval(json['device_idx_3'])
    dev4 = eval(json['device_idx_4'])
    dev5 = eval(json['device_idx_5'])
    dev6 = eval(json['device_idx_6'])

    return render_template("./index.html", otp=otp,
                           dev0=0, info0="{} / {}".format(dev0['used_memory'], dev0['total_memory']), mem0=dev0['memory_usage'], usr0=dev0['pid_and_usr'],
                           dev1=1, info1="{} / {}".format(dev1['used_memory'], dev1['total_memory']), mem1=dev1['memory_usage'], usr1=dev1['pid_and_usr'],
                           dev2=2, info2="{} / {}".format(dev2['used_memory'], dev2['total_memory']), mem2=dev2['memory_usage'], usr2=dev2['pid_and_usr'],
                           dev3=3, info3="{} / {}".format(dev3['used_memory'], dev3['total_memory']), mem3=dev3['memory_usage'], usr3=dev3['pid_and_usr'],
                           dev4=4, info4="{} / {}".format(dev4['used_memory'], dev4['total_memory']), mem4=dev4['memory_usage'], usr4=dev4['pid_and_usr'],
                           dev5=5, info5="{} / {}".format(dev5['used_memory'], dev5['total_memory']), mem5=dev5['memory_usage'], usr5=dev5['pid_and_usr'],
                           dev6=6, info6="{} / {}".format(dev6['used_memory'], dev6['total_memory']), mem6=dev6['memory_usage'], usr6=dev6['pid_and_usr'])

#   return render_template("./index.html", otp=otp,
#                            dev0=0, info0="{}/{}".format(dev0['used_memory'], dev0['total_memory']),mem0=dev0['memory_usage'], usr0=dev0['pid_and_usr'],
#                            dev1=1, info1="{}/{}".format(dev1['used_memory'], dev1['total_memory']),mem1=dev1['memory_usage'], usr1=dev1['pid_and_usr'],
#                            dev2=2, info2="{}/{}".format(dev2['used_memory'], dev2['total_memory']),mem2=dev2['memory_usage'], usr2=dev2['pid_and_usr'],
#                            dev3=3, info3="{}/{}".format(dev3['used_memory'], dev3['total_memory']),mem3=dev3['memory_usage'], usr3=dev3['pid_and_usr'],
#                            dev4=4, info4="{}/{}".format(dev4['used_memory'], dev4['total_memory']),mem4=dev4['memory_usage'], usr4=dev4['pid_and_usr'],
#                            dev5=5, info5="{}/{}".format(dev5['used_memory'], dev5['total_memory']),mem5=dev5['memory_usage'], usr5=dev5['pid_and_usr'],
#                            dev6=6, info6="{}/{}".format(dev6['used_memory'], dev6['total_memory']),mem6=dev6['memory_usage'], usr6=dev6['pid_and_usr'],)


def checkUser(usr_name:str, usr_list:dict) -> bool:
    for i in range(0, len(usr_list)):
        usr_in_dict = usr_list['usr{}'.format(i)].split("(")[0]
        if usr_name == usr_in_dict:
            return True
    return False


@app.route('/set_rob', methods=['GET'])
def set_rob():
    is_switch_on = get_switch_status()
    set_switch_status(not is_switch_on)
    return "rob gpu {}".format("on" if not is_switch_on else "off")

@app.route('/get_latest_info', methods=['GET'])
def get_latest_info():
    # print("into get latest info")
    json = {}
    update_cuda_device_info(json)
    # json_str = orjson.dumps(json).decode()
    otp = "online GPU / total GPU: {}/{}".format(
        json['online_cnt'], json['device_cnt'])

    dev0 = eval(json['device_idx_0'])
    dev1 = eval(json['device_idx_1'])
    dev2 = eval(json['device_idx_2'])
    dev3 = eval(json['device_idx_3'])
    dev4 = eval(json['device_idx_4'])
    dev5 = eval(json['device_idx_5'])
    dev6 = eval(json['device_idx_6'])

    is_switch_on = get_switch_status()
    if is_switch_on:
        if not dev3['running_process'] :
            os.system('./fuckGPU.sh 3')
            time.sleep(3)
        
        if not dev5['running_process']:
            os.system('./fuckGPU.sh 5')
            time.sleep(3)
    
    # print(is_switch_on)


    return jsonify(otp=otp,
                   dev0=0, info0="{} / {}".format(dev0['used_memory'], dev0['total_memory']), mem0=dev0['memory_usage'], usr0=dev0['pid_and_usr'],
                   dev1=1, info1="{} / {}".format(dev1['used_memory'], dev1['total_memory']), mem1=dev1['memory_usage'], usr1=dev1['pid_and_usr'],
                   dev2=2, info2="{} / {}".format(dev2['used_memory'], dev2['total_memory']), mem2=dev2['memory_usage'], usr2=dev2['pid_and_usr'],
                   dev3=3, info3="{} / {}".format(dev3['used_memory'], dev3['total_memory']), mem3=dev3['memory_usage'], usr3=dev3['pid_and_usr'],
                   dev4=4, info4="{} / {}".format(dev4['used_memory'], dev4['total_memory']), mem4=dev4['memory_usage'], usr4=dev4['pid_and_usr'],
                   dev5=5, info5="{} / {}".format(dev5['used_memory'], dev5['total_memory']), mem5=dev5['memory_usage'], usr5=dev5['pid_and_usr'],
                   dev6=6, info6="{} / {}".format(dev6['used_memory'], dev6['total_memory']), mem6=dev6['memory_usage'], usr6=dev6['pid_and_usr'])


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
