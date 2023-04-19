import os
import json as js


import bundle
from getSNMP import consultaSNMP


class state(object):
    agents:dict = None
    data:dict = None

    def __init__(self):

        #try load
        try:
            os.mkdir(bundle.dir.wd)
        except:
            pass
        
        self.__first_cache__()
        self.__first_data__()

    def alias_exists(self, alias:str):
        return alias in self.agents
    
    def p1_qry(self, alias:str):
        if not self.alias_exists(alias):
            print(bundle.Msg.not_exists_err)
            return

        resp = dict()
        for name,oid in bundle.monitor.attr.items():
            resp[name] = self.__qry_agent__(alias, oid)

        ifno = int(int(resp[bundle.monitor.ifno_attr])/2)+1

        ifs = dict()

        for i in range(1, 5):
            si = str(i)
            ifname = self.__qry_agent__(alias, bundle.monitor.ifnm+si)
            ifs[ifname] = self.__qry_agent__(alias, bundle.monitor.ifst+si)
            
        resp[bundle.monitor.ifs] = ifs

        return resp
    
    def update_qry(self, alias:str):
        self.data[alias] = self.p1_qry(alias)
        self.__data__()

    def add_agent(self, alias:str, ip:str, snmp_v:str, community:str, port:str):
        if self.alias_exists(alias):
            return bundle.Msg.exists_err

        ins = list((ip, snmp_v, community, port))
        err = 0
        for v in self.agents.values():
            for u, i in zip(v.values(), ins):
                if str(u) == str(i):
                    err += 1
        
        if err == 3:
            return bundle.Msg.vals_err

        self.agents[alias] = {
            bundle.keys.ip: ip,
            bundle.keys.ver: snmp_v,
            bundle.keys.com: community,
            bundle.keys.port: port,
        }
        self.__cache__()

        self.data[alias] = self.p1_qry(alias)

        self.__data__()


        return ''
    
    def rem_agent(self, alias:str):
        if self.alias_exists(alias):
            self.agents.pop(alias)
            self.data.pop(alias)
            self.__cache__()
            self.__data__()
            return ''
        else:
            print(bundle.Msg.not_exists_err)
            return bundle.Msg.not_exists_err
    
    def mod_agent(self, alias:str, ip:str, snmp_v:str, community:str, port:str):
        self.rem_agent(alias)
        self.add_agent(alias, ip, snmp_v, community, port)
        

    #p2
    def p2_qry(self, alias:str):
        if not self.alias_exists(alias):
            print(bundle.Msg.not_exists_err)
            return
        
        data = dict()
        for names,oids in zip(bundle.p2.varnames.arr, bundle.p2.oids.arr):
            data[names] = self.__qry_agent__(alias, oids)

        return data

    def __qry_agent__(self, alias:str, oid:str):
        if alias not in self.agents:
            print(bundle.Msg.not_exists_err)
            return

        args = self.agents[alias]
            
        return consultaSNMP(args[bundle.keys.com], args[bundle.keys.ip], oid, args[bundle.keys.port])

    def str_agent(self, alias:str):
        v = self.data[alias]
        s = f'\t===============   {alias}   ===============\n'
        s = f'{s}comunidad: {self.agents[alias][bundle.keys.com]}'
        for f,u in zip(bundle.monitor.attr, v.values()):
            s = f'{s}\n{f}: {u}'
        s = f'{s}\n\t*interfaces'
        for ki, ii in v[bundle.monitor.ifs].items():
            s = f'{s}\n{ki}:  {"up" if ii=="1" else "down"}'
        s = f'{s}\n'
        return s

    def list_agents(self) -> str:
        s = f''
        for k in self.data.keys():
            s = f'{s} {self.str_agent(k)}'
        return s


    def __cache__(self):
        with open(f'{bundle.dir.wd}/{bundle.dir.cache}', 'w') as fd:
            fd.write(js.dumps(self.agents))

    def __data__(self):
        with open(f'{bundle.dir.wd}/{bundle.dir.data}', 'w') as fd:
            fd.write(js.dumps(self.data))

    def __dbg_str__(self):
        return str(self.agents)

    def __first_cache__(self):
        try:
            with open(f'{bundle.dir.wd}/{bundle.dir.cache}', 'r') as fd:
                sjs:str = fd.read(-1)
                self.agents = js.loads(sjs)
        except:
            self.agents = dict()
            self.__cache__()

    def __first_data__(self):
        try:
            with open(f'{bundle.dir.wd}/{bundle.dir.data}', 'r') as fd:
                sjs:str = fd.read(-1)
                self.data = js.loads(sjs)
        except:
            self.data = dict()
            self.__data__()


