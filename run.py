from util import doc_util as doc
from util import ethscrap_util as es

token_name='LostSoul'
token_address='0x5a263050f6bfa6ccd262de9f5451c65e5831c817'

#get all hashs of token
# hashs=es.get_hash_all(token_address)
# doc.savelist(hashs,token_name)

#get all transations from downloaded hashs
hashs=doc.loadlist(token_name)
totaltx=es.get_tx(hashs[0])
for txhash in hashs[1:]:
    print(txhash)
    tx=es.get_tx(txhash)
    totaltx=totaltx.append(tx)

#adjust format of transation data
totaltx=doc.adjust_txdata(totaltx,token_address)

#save transation data
doc.savecsv(totaltx,token_name)
