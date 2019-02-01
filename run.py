import ethscrap as es
import os
import pickle


token=''

def main():
    hashlist=es.get_hash_all(token)
    for hash in hashlist:

