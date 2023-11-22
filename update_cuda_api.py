import pynvml
import psutil
import orjson


B_TO_MB = 1024 * 1024
LOST_DEVICE = "LOST DEVICE"


class update_cuda_device_info():
    def __init__(self, device_Json) -> None:
        self.device_json = device_Json
        self.handle_list = []
        self.memory_usage_list = []
        self.device_pid_list = []
        self.device_count = 0
        self.online_count = 0

        if self.get_device_handle():
            for handle in self.handle_list:
                self.memory_usage_list.append(self.get_device_memory(handle))
                self.device_pid_list.append(self.get_device_pid(handle))
            # for pid_list in self.device_pid_list:
            #     print(pid_list)
            # for mem_list in self.memory_usage_list:
            #     print(mem_list)
            self.to_Json()

    def get_device_handle(self) -> bool:
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        if device_count <= 0:
            return False
        else:
            self.device_count = device_count
            for i in range(0, device_count):
                try:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    self.handle_list.append(handle)
                    self.online_count = self.online_count + 1
                except:
                    self.handle_list.append(LOST_DEVICE)
            return True

    def get_device_memory(self, handle) -> list:
        sub_memory_list = []
        if handle == LOST_DEVICE:
            return sub_memory_list

        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        mem_used = mem_info.used / B_TO_MB
        mem_total = mem_info.total / B_TO_MB
        mem_usage = (mem_used / mem_total) * 100

        sub_memory_list.append(round(mem_used, 2))
        sub_memory_list.append(round(mem_total, 2))
        sub_memory_list.append(round(mem_usage, 2))


        return sub_memory_list

    def get_device_pid(self, handle) -> list:
        pid_list = []
        if handle == LOST_DEVICE:
            return pid_list
        running_processes = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
        for process in running_processes:
            pid = process.pid
            usr = psutil.Process(pid).username()
            pid_list.append([pid, usr])
        return pid_list

    def to_Json(self):
        self.device_json['device_cnt'] = self.device_count
        self.device_json['online_cnt'] = self.online_count
        for i in range(0, self.device_count):
            running_process = "False"
            if self.handle_list[i] == LOST_DEVICE:
                tmp_str = 'device_idx_{}'.format(i)
                sub_str = '''
                'used_memory':'OFFLINE',
                'total_memory':'OFFLINE',
                'memory_usage':'OFFLINE',
                'pid_and_usr' : 'OFFLINE',
                'running_process' : 'OFFLINE'
                '''
                self.device_json[tmp_str] = '{' + sub_str + '}'
                continue
            else:
                pid_str = "{"
                pid_info_len = len(self.device_pid_list[i])
                if pid_info_len > 0:
                    running_process = "True"
                    for j in range(0, len(self.device_pid_list[i])):
                        pid_tmp_str = "'usr{}':'{}({})',".format(
                            j, self.device_pid_list[i][j][1], self.device_pid_list[i][j][0])
                        pid_str = pid_str + pid_tmp_str
                else:
                    pid_str = pid_str + "'usr0':'empty'"
                pid_str = pid_str + '}'

                tmp_str = 'device_idx_{}'.format(i)
                sub_str = '''
                'used_memory':'{} MB',
                'total_memory':'{} MB',
                'memory_usage':'{}%',
                'pid_and_usr' : {},
                'running_process' : {}
                '''.format(self.memory_usage_list[i][0], self.memory_usage_list[i][1], self.memory_usage_list[i][2], pid_str, running_process)

                self.device_json[tmp_str] = '{' + sub_str + '}'


if __name__ == '__main__':
    json = {}
    update_cuda_device_info(json)
    json_str = orjson.dumps(json).decode()
    with open("./info.json", "w") as f:
        f.write(json_str)
    # json_str = orjson.dumps(json)
    # json_str = orjson.loads(json_str)
    dev1 = eval(json['device_idx_1'])
    print(dev1['pid_and_usr'])
