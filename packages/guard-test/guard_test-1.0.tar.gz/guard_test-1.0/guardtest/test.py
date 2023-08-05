import os, sys, getopt
from androguard.misc import AnalyzeAPK
from androguard.core.bytecodes.apk import APK
from androguard.core.analysis.analysis import Analysis
from androguard.core.bytecodes.dvm import DalvikVMFormat

APK_PATH = "/Users/huangxiaoming/project/python/androguard_test/guardtest/mobile5.6.3.apk"
CLASS_NAME = "Lcom/facebook/imagepipeline/core/ImagePipeline;"
METHOD_NAME = "isInBitmapMemoryCache"

SHELL_TIP = 'test.py -i <apk> -c <class> -m <method>'


def analyze(apk_path=None, class_name=None, method_name=None):
    if not apk_path:
        print('apk_path cannot empty')
        return
    if not class_name:
        print('class_name cannot empty')
        return
    if not method_name:
        print('method_name cannot empty')
        return
    print("分析开始了，耐心等待吆...")
    a, d, dx = AnalyzeAPK(apk_path)
    # a = APK('./mobile5.6.3.apk')
    # d = DalvikVMFormat(a.get_dex())
    # dx = Analysis(d)
    # permissions = a.get_permissions()
    # print(permissions)

    xref_log = method_name + '\n'
    env = dx.classes[class_name]
    for method in env.get_methods():
        print('method {}'.format(method.name))
        if method_name == method.name:
            for _, call, _ in method.get_xref_from():
                call_by = "called by --> {} -- {}\n".format(call.class_name, call.name);
                xref_log += call_by
                print(call_by)

    write_log(xref_log)


def write_log(log):
    file_path = 'log.txt'
    print(file_path)
    with open(file_path, 'w') as f:
        f.write(log)


def get_options(argv):
    print(argv)
    try:
        opts, args = getopt.getopt(argv, "i:m:c:h")
    except getopt.GetoptError:
        print(SHELL_TIP)
        sys.exit(2)

    for opt, arg in opts:
        if '-h' == opt:
            print(SHELL_TIP)
            sys.exit()
        elif '-c' == opt:
            class_name = arg
        elif '-i' == opt:
            apk_path = arg
        elif '-m' == opt:
            method = arg

        print("opt: {} --> arg:{}".format(opt, arg))

    return apk_path, class_name, method


if __name__ == '__main__':
    print("简单例子：test.py -i {} -c '{}'; -m {}".format(APK_PATH, CLASS_NAME, METHOD_NAME))
    apk, clazz, meth = get_options(sys.argv[1:])
    analyze(apk, clazz, meth)

    # print(os.getcwd())
    # print(sys.argv[0])
    # print(__file__)
    # print(sys.path[0])

    # write_log("hello")
