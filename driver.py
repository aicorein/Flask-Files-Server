import psutil
import os


def get_winDriver():
    """
    Windows操作系统下,返回全部驱动器卷标['C:\','D:\']
    """
    # 返回驱动器卷标列表
    driver_list = sorted([driver.device for driver in psutil.disk_partitions(True)])
    
    for index in range(len(driver_list)):
        # 重新格式化分隔符
        driver_list[index] = driver_list[index].strip('\\')
        driver_list[index] += '/'

        # 测试各驱动器是否可访问，目的是筛除未就绪驱动器，如空光驱
        try:
            os.listdir(driver_list[index])
        except PermissionError as e:
            if '[WinError 21]' in str(e):
                del driver_list[index]
            # 异常类型不为 “设备未就绪” 的再次抛出异常供调试
            else:
                raise (PermissionError, e)

    # 返回列表
    return driver_list


if __name__ == "__main__":
    paths = get_winDriver()
    print(paths)


