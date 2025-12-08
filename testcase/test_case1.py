import pytest
def test_case_hello():
    print("这里是case1:This is a failed case")
    assert False
# 主函数运行
if __name__ == "__main__":
    pytest.main(['-vs'])
    # 参数含义：-v 输出调试信息
    # -s,输出更详细的信息，文件名、用例名
    # -n 多线程执行
    # -x 执行中有用例失败，立刻停止运行
    # -x=[number] 有number个失败，立刻停止运行
    # -html=[filepath/report.html] 在filepath生成report.html的测试报告


# 控制台运行
#  pytest .\testcase\test_case1.py -vs