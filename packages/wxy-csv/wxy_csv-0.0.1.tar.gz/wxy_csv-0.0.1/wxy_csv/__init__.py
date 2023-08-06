# coding=utf-8
import csv


class CSV:

    @staticmethod
    def select(file,param,serial_num,head=True):
        '''
        :param file: 文件路径                    @ str
        :param param: 行、列                     @ str
        :param serial_num: 行数、列数            @ list
        :param head:True为去除表头，False为保留表头     @ bool
        :return: 可一次取多行(列)，返回指定行(列)数据                 @ list
        '''
        if isinstance(serial_num,list)==False:
            raise TypeError('以列表形式传入serial_num')
        for i in serial_num:
            if isinstance(i,int)==False and i<1:
                raise TypeError('serial_num元素应为大于0的整数')

        if param == "行":
            result = []
            for j in serial_num:
                reader = csv.reader(open(file, mode='r', encoding='utf-8'))
                try:
                    for i in range(j):
                        row = next(reader)  # next方法返回文件中的下一行
                    result.append(row)
                except:
                    result.append([None])

            return result

        elif param == "列":
            result = []
            for j in serial_num:
                reader = csv.reader(open(file, mode='r', encoding='utf-8'))
                column = []
                try:
                    for i in reader:
                        column.append(i[j - 1])
                    if head == True:
                        column.pop(0)
                    result.append(column)
                except:
                    result.append([None])
            return result

    # @staticmethod
    # def new_csv(file, data):
    #
    #     # 创建csv并且录入表头
    #     with open(file, 'a', newline="") as csv_file:
    #         csv.writer(csv_file).writerow(data)
    #
    #
    # @staticmethod
    # def entry_csv(file, data):
    #     with open(file, "a", newline='') as csv_file:
    #         csv.writer(csv_file).writerow(data)
