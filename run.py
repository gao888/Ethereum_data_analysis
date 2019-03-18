from util import doc_util as doc
from util import spider_util as sp
from util import balance_util as ba
token_name='SeeleToken'
token_address='0xb1eef147028e9f480dbc5ccaa3277d417d1b85f0'

#get all transactions of token
table=sp.main(token_address)

#save all transactions
doc.savecsv(table,token_name+'_tx')

#load all transactions
totaltx=doc.loadcsv(token_name+'_tx')

#get daily balance
balance=ba.main(totaltx)
doc.savecsv(table,token_name+'_balance')





#get all hashs of token
# hashs=es.get_hash_all(token_address)
# doc.savelist(hashs,token_name)

#get all transations from downloaded hashs
# hashs=doc.loadlist(token_name)
# totaltx=es.get_tx(hashs[0])
# for txhash in hashs[1:]:
#     print(txhash)
#     tx=es.get_tx(txhash)
#     totaltx=totaltx.append(tx)