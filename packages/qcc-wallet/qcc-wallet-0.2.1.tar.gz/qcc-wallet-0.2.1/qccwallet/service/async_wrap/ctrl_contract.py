# coding:utf-8

from .. import ctrl_contract
from asyncio import get_event_loop


async def register(cid, data, *auth_args):
    args = cid, data, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_contract.register, *args)


async def unregister(cid, contract_id, *auth_args):
    args = (cid, contract_id, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_contract.unregister, *args)


async def read(cid, contract_id, *auth_args):
    args = (cid, contract_id, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_contract.read, *args)


async def query_contracts(cid, *auth_args):
    args = (cid, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_contract.query_contracts, *args)
