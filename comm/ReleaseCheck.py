# encoding:utf-8
"""
@author = Monika
@create = 2019/9/29 13:09
"""
from unrar import rarfile
from comm.OperatFile import ReadFile
from comm.PubFunctions import PubFunctions
from comm.logger import Logger
import os
import sys


class ReleaseCheck:
    
    def __init__(self):
        self.rf = ReadFile()
        if self.rf.readini('ReleaseCheck') is None:
            self.rc = None
        else:
            self.rc = self.rf.readini('ReleaseCheck')
        self.status = 0
        self.lg = Logger('info')
        
    def getpath(self):
        return os.path.split(sys.argv[0])[0]
    
    def isPswRight(self):
        try:
            pf = PubFunctions()
            if self.rc is None:
                self.lg.info('未找到文件config.ini，开始检查当前路径')
                psw_path = os.path.split(pf.getFilePath(name='.txt')[0])[0]
                filepath = None
            else:
                filepath = self.rc['filepath']
                psw_path = filepath
            rar_path = pf.getFilePath(filepath, name='.rar')[0]
            self.lg.info('*********Start************')
            self.lg.info(f'1.检查压缩文件{os.path.split(rar_path)[1]}解压密码')
            psw = self.rf.readtxt(psw_path)[0]
            if len(psw) == 60:
                self.lg.info(' (1)pass：密码长度=60')
            else:
                self.lg.info(f' (1)fail：密码长度为{len(psw)}≠60')
            try:
                rarf = rarfile.RarFile(rar_path, 'r', psw)
                self.extra_path = os.path.splitext(rar_path)[0]
                if os.path.exists(self.extra_path):
                    self.lg.info(' (2)pass：密码正确，已存在解压文件夹，不再重复解压')
                else:
                    rarf.extractall(self.extra_path)
                    self.lg.info(f' (2)pass：密码正确，解压文件到{self.extra_path}')
            except Exception as e:
                self.lg.info(f' (2)fail：密码错误，解压失败:{e}！')
                pass
        except Exception as e:
            self.lg.info(f'Error:{e}！')
            pass
            
    def isContain(self):
        
        try:
            if self.rc is None:
                checkstr_list = ['clinet', 'test', 'key', 'nokey', 'debug', 'log', 'svn', 'demo', '.dmp',
                             '.ilk', '.pdb', '.log', '.dump', 'logfile', 'bin']
            else:
                checkstr_list = self.rc['checkstring'].split(',')
            self.lg.info(f'2.检查关键字{checkstr_list}')
            if os.path.exists(self.extra_path):
                for root, dirs, files in os.walk(self.extra_path, topdown=True):
                    if files:
                        for f in files:
                            filename = f.lower()
                            for k in checkstr_list:
                                if filename.find(k) != -1:
                                    self.lg.info(f'  文件{filename}包含{k}，路径：{root}')
                                    self.status = 1
            else:
                self.lg.info(f'解压失败，不再进行关键字检查')
                return
            if self.status == 0:
                self.lg.info('pass：版本包关键字检查通过!')
            else:
                self.lg.info('fail：版本包关键字检查不通过!')
            os.startfile("C:\Program Files (x86)\Beyond Compare 4\BCompare.exe")
        except Exception as e:
            self.lg.error('error: %s' % e)
            pass
        finally:
            self.lg.info('*********End************\n')
            input('Press Enter to exit...')
 
            
if __name__ == '__main__':
    rc = ReleaseCheck()
    rc.isPswRight()
    rc.isContain()
