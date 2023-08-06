import lmfhawq.zl as src 

import lmfhawq.zldb as v 

from lmfhawq.data import zhulong_diqu_dict



src_add_quyu=src.add_quyu_fast 


src_drop_quyu=src.drop_quyu_fast


v_add_quyu=v.add_quyu 

v_drop_quyu=v.drop_quyu 




def src_add_sheng(sheng,tag):
    quyus=zhulong_diqu_dict['sheng']
    for quyu in quyus:

        src_add_quyu(quyu,tag)

def v_add_sheng(sheng,tag):
    quyus=zhulong_diqu_dict['sheng']
    for quyu in quyus:

        v_add_quyu(quyu,tag)




