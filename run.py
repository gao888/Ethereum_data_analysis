import ethscrap_util as es
import doc_util as doc


token_name='seele'
token_address='0xb1eef147028e9f480dbc5ccaa3277d417d1b85f0'
#get all hash of token
hashs=es.get_hash_all(token_address)
doc.savelist(hashs,token_name)

hashs=doc.loadlist(token_name)
totaltx=es.get_tx(hashs[0])
for txhash in hashs[1:]:
    tx=es.get_tx(txhash)
    totaltx=totaltx.append(tx)
    
doc.savedata(totaltx,token_name)