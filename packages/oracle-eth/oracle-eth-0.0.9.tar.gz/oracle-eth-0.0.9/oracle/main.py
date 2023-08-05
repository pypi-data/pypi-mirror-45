#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from oracle.business import BaseEvent, ArmyEvent, import_event, OrganizationEvent
from oracle import setting
import click
from oracle import cusomer
from oracle.setting import VAR
from pycontractsdk.contracts import Contract
from oracle.database import dbs
from oracle.plugins import Processor
# from oracle.plugins.solider import Solider
import importlib
import os
import re
from oracle.utils import import_plugins




@click.command()
@click.option('-f', "--file", default='/etc/oracle_army.conf', help='指定配置文件的路径（默认: /etc/oracle_army.conf）')
def army(file):
    # TODO: 军队 运行的验证程序"
    # 初始化配置信息
    setting.read_config2(file)
    print(setting.VAR)
    # army = ArmyEvent()
    # army.monitor_event('DIDAttributeChange')

    import_plugins()
    event = BaseEvent()
    event.monitor_event('DIDAttributeChange')


@click.command()
@click.option('-f', "--file", default='/etc/oracle.conf', help='指定配置文件的路径（默认: /etc/oracle.conf）')
def organization(file):
    # TODO: 机构 运行的oracle程序"
    # 初始化配置信息
    import_plugins()
    setting.read_config2(file)
    print(setting.VAR)
    organization = OrganizationEvent()
    organization.monitor_event('DIDAttributeConfirmed')


@click.command()
@click.option('-f', "--file", default='/etc/oracle.conf', help='指定配置文件的路径（默认: /etc/oracle.conf）')
def impevent(file):
    """
    导入event数据到数据库中
    :param file: 配置文件的路径
    :return:
    """
    # global PATH
    # setting.PATH = os.path.dirname(os.path.abspath(__file__))
    import_plugins()
    # 初始化配置信息
    setting.read_config2(file)
    # business.monitor_event('DIDOwnerChanged')
    import_event()


@click.command()
@click.option('-f', "--file", default='/etc/oracle.conf', help='指定配置文件的路径（默认: /etc/oracle.conf）')
def upload_chain(file):
    """
    消费队列中的数据，进行上链操作
    :param file:
    :return:
    """
    import_plugins()
    # 初始化配置信息
    setting.read_config2(file)
    # 实例化 Contract
    provider = VAR['ETH_PROVIDER']
    contract_address = VAR['CONTRACT_ADDRESS']
    abi = VAR['CONTRACT_ABI']
    operator_private_key = VAR['OPERATOR_PRIVATEKEY']
    delegate_private_key = VAR['DELEGATE_PRIVATEKEY']
    gas = VAR['GAS']
    gas_prise = VAR['GAS_PRISE']
    concart = Contract(provider=provider, timeout=60, contract_address=contract_address, abi=abi,
                  private_key=operator_private_key,
                  gas=int(gas),
                  gas_prise=int(gas_prise)
                  )
    # 启动 消费者程序
    cus = cusomer.CallContract(
        contracrt=concart,
        queue_name=VAR['QUEUE_NAME'],
        queue_ip=VAR['QUEUE_IP'],
        queue_port=VAR['QUEUE_PORT'],
        queue_user=VAR['QUEUE_USER'],
        queue_password=VAR['QUEUE_PASSWORD'],
        queue_vhost=VAR['QUEUE_VHOST'],
    )
    cus.cusomer()
    # from concurrent.futures import ProcessPoolExecutor
    # with ProcessPoolExecutor(max_workers=5) as executor:
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)


@click.command()
@click.option('-f', "--file", default='/etc/oracle.conf', help='指定配置文件的路径（默认: /etc/oracle.conf）')
def validation_chain(file):
    """ 用于验证数据是否上链 """
    import_plugins()
    # 初始化配置信息
    setting.read_config2(file)

    # 实例化 Contract
    provider = VAR['ETH_PROVIDER']
    contract_address = VAR['CONTRACT_ADDRESS']
    abi = VAR['CONTRACT_ABI']
    operator_private_key = VAR['OPERATOR_PRIVATEKEY']
    delegate_private_key = VAR['DELEGATE_PRIVATEKEY']
    gas = VAR['GAS']
    gas_prise = VAR['GAS_PRISE']
    concart = Contract(provider=provider, timeout=60, contract_address=contract_address, abi=abi,
                       private_key=operator_private_key,
                       gas=gas,
                       gas_prise=gas_prise
                       )
    # 启动 消费者程序
    cus = cusomer.ValidationContract(
        contracrt=concart,
        queue_name=VAR['QUEUE_NAME_VALIDATION'],
        queue_ip=VAR['QUEUE_IP'],
        queue_port=VAR['QUEUE_PORT'],
        queue_user=VAR['QUEUE_USER'],
        queue_password=VAR['QUEUE_PASSWORD'],
        queue_vhost=VAR['QUEUE_VHOST'],
    )
    cus.cusomer()
    # from concurrent.futures import ProcessPoolExecutor
    # with ProcessPoolExecutor(max_workers=5) as executor:
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)

@click.command()
@click.option('-f', "--file", default='/etc/oracle.conf', help='指定配置文件的路径（默认: /etc/oracle.conf）')
def validation_chain2(file):
    import_plugins()
    # 初始化配置信息
    setting.read_config2(file)
    from oracle.cusomer import ValidationChainWorker
    jobs = []
    for i in range(3):
        p = ValidationChainWorker(i)
        jobs.append(p)
        p.start()
        print("count : {}".format(len(jobs)))
    for j in jobs:
        j.join()
    print("count22 : {}".format(len(jobs)))

if __name__ == "__main__":
    # impevent()
    army()
    # army('/Users/yuyongpeng/git/hard-chain/cport/oracle/oracle_army.conf')
    # organization('/Users/yuyongpeng/git/hard-chain/cport/oracle/oracle.conf')
    # upload_chain()
    # validation_chain2()
