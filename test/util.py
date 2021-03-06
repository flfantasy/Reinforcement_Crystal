import argparse
import os

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def gen_data(dataset, scale_factor):
    path = './' + dataset + '/dbgen/'
    with cd(path):
        os.system('rm -rf *.tbl')
        if dataset == 'ssb':
            os.system('./dbgen -s %d -T a' % scale_factor)
        else :  # tpch
            os.system('./dbgen -s %d' % scale_factor)
        os.system('mkdir -p ../data/s%d' % scale_factor)
        os.system('mv *.tbl ../data/s%d/' % scale_factor)

def transform(dataset, scale_factor):
    path = './' + dataset + '/loader/'
    ip = '../data/s%d/' % scale_factor
    op = '../data/s%d_columnar/' % scale_factor
    with cd(path):
        os.system('mkdir -p %s' % op)
        # 将一些字符串列转换为int
        os.system('python3 convert.py ../data/s%d/' % scale_factor)
        # 将行式存储转换为列式存储
        if dataset == 'ssb':
            os.system('./loader --lineorder %s/lineorder.tbl --ddate %s/date.tbl --customer %s/customer.tbl.p --supplier %s/supplier.tbl.p --part %s/part.tbl.p --datadir %s' % (ip, ip, ip, ip, ip, op))
        else :  # tpch
            os.system('./loader --lineitem %s/lineitem.tbl.p --orders %s/orders.tbl.p --customer %s/customer.tbl.p --part %s/part.tbl.p --partsupp %s/partsupp.tbl --supplier %s/supplier.tbl.p --nation %s/nation.tbl.p --region %s/region.tbl.p --datadir %s' % (ip, ip, ip, ip, ip, ip, ip, ip, op))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'data gen')
    parser.add_argument('dataset', type=str, choices=['ssb', 'tpch'])
    parser.add_argument('scale_factor', type=int)
    parser.add_argument('action', type=str, choices=['gen', 'transform'])
    args = parser.parse_args()

    if args.action == 'gen':
        gen_data(args.dataset, args.scale_factor)
    elif args.action == 'transform':
        transform(args.dataset, args.scale_factor)

