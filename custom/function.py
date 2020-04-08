# coding: utf-8

"""
说明: 用于监控系统通用函数定义
作者: zz
版本: v4.0.0
"""

## 调用python模块
import os, sys
import time, io, json, shutil, uuid
import logging

## 从全局配置中调用变量
from monitor import cfg, cacheTime

## 指定日志格式
cfg.logFormat

## 判断缓存脚本是否执行函数
## 返回True执行, 返回False不执行
def cache_exec(**kwargs):
    ## 获取参数
    _label    = kwargs.get('label')
    _stepTime = kwargs.get('stepTime') or cacheTime

    ## 当前unixtime
    _curTime  = time.time()
    ## 项目json文件位置
    _jsonPath = os.path.join(cfg.cachePath, _label)
    _fileName = cfg.curCache.format(_label)
    _jsonFile = os.path.join(_jsonPath, _fileName)

    ## 判断缓存文件是否存在, 是否过期
    if os.path.isfile(_jsonFile):
        try:
            ## 读取已有项目缓存数据
            with open(_jsonFile,'r') as _f:
                _dataDict = json.loads(_f.read())
        except ValueError as e:
            ## 读取失败删除原有文件并返回True
            os.remove(_jsonFile)
            return True
        else:
            ## 读取成功比较当前时间和文件中缓存的时间差是否大于预设时间
            try:            
               _diffTime = _curTime - _dataDict.get('unixtime')
            except Exception as e:
                return True
            else:
                if _diffTime >= float(_stepTime):
                    return True
                else:
                    return False
    else:
        return True

## 创建缓存文件函数
def cache_file(**kwargs):
    ## 获取参数
    _label = kwargs.get('label')
    _data  = kwargs.get('data')

    ## 获取cache路径和tmp路径
    _jsonPath = os.path.join(cfg.cachePath, _label)
    _tmpPath  = cfg.tmpPath

    ## 设置当前缓存文件和之前缓存文件名称
    _curFile = cfg.curCache.format(_label)
    _preFile = cfg.preCache.format(_label)

    ##修正文件路径为绝对路径
    _curFile = os.path.join(_jsonPath, _curFile)
    _preFile = os.path.join(_jsonPath, _preFile)

    ## 设置临时文件名称
    _random  = ''.join(str(uuid.uuid4()).split('-'))
    _tmpFile = '{}_{}.json'.format(_tmpPath, _random)

    ## 确定缓存路径存在
    if not os.path.exists(_jsonPath):
        os.makedirs(_jsonPath)
    
    ## 确定临时路径存在
    if not os.path.exists(_tmpPath):
        os.makedirs(_tmpPath)

    ## 写入数据到临时文件
    open(_tmpFile, 'w').write(json.dumps(_data))

    ## 写入数据到之前缓存文件
    if os.path.isfile(_curFile):
        shutil.move(_curFile, _preFile)
    else:
        shutil.copy(_tmpFile, _preFile)

    ## 写入数据到当前缓存文件
    shutil.move(_tmpFile, _curFile)

## 转换psutil元组格式为字典
def psutil_to_dict(_tuple):
    ## 读取参数(psutil元组)
    _str      = str(_tuple)

    ## 将数据处理为列表
    _startStr = (_str.find('(')) + 1
    _endStr   = (_str.find(')'))
    _list     = _str[ _startStr : _endStr ].replace('=', ',').replace(' ', '').split(',')

    ## 生成字典的索引列表和值列表
    _indexList = [ _x for _x in _list if _list.index(_x)%2 == 0 ]
    _keyList   = [ _x for _x in _list if _list.index(_x)%2 != 0 ]

    ## 生成字典
    _dict = dict(zip(_indexList, _keyList))

    ## 返回数据
    return _dict

## 度量转换(转换kB, mB, gB, tB为bytes)
def convert_bytes(_data, _unit):
    unitDict={
        'b'  : 1024**0,
        'kb' : 1024**1,
        'mb' : 1024**2,
        'gb' : 1024**3,
        'tb' : 1024**4,
        'pb' : 1024**5,
        'eb' : 1024**6,
        'zb' : 1024**7,
        'yb' : 1024**8,
        'bb' : 1024**9
    }

    _unit=_unit.lower()
    
    try:
        return float(_data) * unitDict.get(_unit)
    except TypeError as e:
        logging.error('类型错误, 转换失败: value={}, unit={}'.format(_data, _unit))
        logging.error(e)

## 获取json文件数据，并转置为数组形式
def load_json_file(_fileName):
    try:
        _file = io.open(_fileName, 'rt', encoding = 'utf-8').read()
    except FileNotFoundError:
        logging.error(
            '缓存文件不存在: file={}'.format(
            _fileName)
        )
    else:
        try:
            _dict = json.loads(_file)
            return _dict
        except json.decoder.JSONDecodeError:
            logging.error(
                '缓存文件不是json数据: file={}'.format(
                _fileName)
            )
## 获取索引
def get_index(**kwargs):
    ## 获取参数
    _jsonFile = kwargs.get('jsonFile')

    ## 获取数据字典
    _dict = load_json_file(_jsonFile)

    ## 获取数据
    if _dict:
        try:
            _indexList = [ x for x in _dict.get('data').keys() ]
            _result    = _indexList
            return _result
        except:
            logging.error(
                '获取关键词列表失败: jsonFile={}'.format(
                _jsonFile)
            )

## 获取二级索引
def get_sec_index(**kwargs):
    ## 获取参数
    _jsonFile = kwargs.get('jsonFile')
    _arg1 = kwargs.get('arg1')

    ## 获取数据字典
    _dict = load_json_file(_jsonFile)

    ## 获取数据
    if _dict:
        try:
            _indexList = [ x for x in _dict.get('data').get(_arg1).keys() ]
            _result = _indexList
            return _result
        except:
            logging.error(
                '获取次关键词列表失败: jsonFile={}, arg1={}'.format(
                _jsonFile, _arg1)
            )

def get_initdata(**kwargs):
    ## 获取参数
    _arg1     = kwargs.get('arg1')
    _arg2     = kwargs.get('arg2')
    _jsonFile = kwargs.get('jsonFile')

    ## 获取数据字典
    _dict = load_json_file(_jsonFile)

    ## 获取数据
    if _dict:
        try:
           _value  = _dict.get('data').get(_arg1).get(_arg2)
        except:
            logging.error(
                '缓存数据没有对应参数的查询值: jsonFile={}, arg1={}, arg2={}'.format(
                _jsonFile, _arg1, _arg2)
            )
        else:
            _result = _value
            return _result

def get_diffdata(**kwargs):
    ## 获取参数
    _arg1    = kwargs.get('arg1')
    _arg2    = kwargs.get('arg2')
    _curFile = kwargs.get('curFile')
    _preFile = kwargs.get('preFile')

    ## 当前数据
    _curDict = load_json_file(_curFile)

    ## 之前数据
    if _curDict:
        _preDict = load_json_file(_preFile)

    ## 计算差值
    if _preDict:
        try:
           _curValue  = _curDict.get('data').get(_arg1).get(_arg2)
           _preValue  = _preDict.get('data').get(_arg1).get(_arg2)
           _diffValue = float(_curValue) - float(_preValue)
        except:
            logging.error(
                '缓存数据没有对应参数的查询值: curFile={}, preFile={}, arg1={}, arg2={}'.format(
                _curFile, _preFile, _arg1, _arg2)
            )
        else:
            if _diffValue >= 0:
                _result = _diffValue
            else:
                _result = 0.0
                logging.warning(
                    '负数归零(出现负数通常是由于系统第一次获取数据或者系统刚刚重启时某些变量被重置导致): _diffValue={}'.format(
                    _diffValue)
                )
            return _result

def get_avgdata(**kwargs):
    ## 获取参数
    _arg1    = kwargs.get('arg1')
    _arg2    = kwargs.get('arg2')
    _curFile = kwargs.get('curFile')
    _preFile = kwargs.get('preFile')

    ## 当前数据
    _curDict = load_json_file(_curFile)

    ## 之前数据
    if _curDict:
        _preDict = load_json_file(_preFile)

    ## 计算差值
    if _preDict:
        try:
            _curValue  = _curDict.get('data').get(_arg1).get(_arg2)
            _preValue  = _preDict.get('data').get(_arg1).get(_arg2)
            _diffValue = float(_curValue) - float(_preValue)
    
            _curTime  = _curDict.get('unixtime')
            _preTime  = _preDict.get('unixtime')
            _diffTime = float(_curTime) - float(_preTime)
        except:
            logging.error(
                '缓存数据没有对应参数的查询值: _curFile={}, _preFile={}, arg1={}, arg2={}'.format(
                _curFile, _preFile, _arg1, _arg2)
            )
        else:
            if _diffValue >= 0:
                try:
                    _result = round(_diffValue / _diffTime, 2)
                except ZeroDivisionError:
                    _result = 0.0
                    logging.warning(
                        '除数为零: _diffTime={}'.format(
                        _diffTime)
                    )
            else:
                _result = 0.0
                logging.warning(
                    '负数归零(负数通常是系统第一次获取数据或者系统刚刚重启时变量重置导致): _diffValue={}'.format(
                    _diffValue)
                )
            return _result

## 取列表嵌套字典的字典中某元素排行榜
def list_dict_top(_list, _dictKey, _count):
    ## 逆向排序并取列表前 _count 值
    _sortList = sorted(_list, key=lambda x:x.get(_dictKey),reverse=True)[:5]
    ## 修改原列表格式为列表嵌套元组格式, 并修正排序值浮点长度
    _result   = [ (x.get('name'), round(x.get(_dictKey), 2)) for x in _sortList ]
    ## 返回结果
    return _result

## 本地调试
if __name__ == '__main__':
    print(__doc__)
