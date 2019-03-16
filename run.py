from util import doc_util as doc
from util import ethscrap_util as es

token_name='SeeleToken'
token_address='0xb1eef147028e9f480dbc5ccaa3277d417d1b85f0'

#get all transactions of token
table=es.main(token_address)

#save all transactions
filename=token_name+'_tx'
doc.savecsv(table,filename)
#adjust format of transation data
# totaltx=doc.adjust_txdata(totaltx,token_address)

#save transation data
# doc.savecsv(totaltx,token_name)


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