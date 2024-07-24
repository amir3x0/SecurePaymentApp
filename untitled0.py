# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:57:40 2024

@author: Shimron-Ifrrah
"""

from schnorr import SchnorrSignature , generate_schnorr_parameters
messge = "message"
p_schnorr ,q_schnorr ,a_schnorr  = generate_schnorr_parameters(16)
sender_schnorr = SchnorrSignature(p_schnorr,q_schnorr,a_schnorr)
sender_schnorr.generate_keys()
e,y,X = sender_schnorr.sign(messge)

schnorr_receiver = SchnorrSignature(p_schnorr,q_schnorr,a_schnorr)
is_valid =schnorr_receiver.verify(messge,e,y,X,sender_schnorr.v)
print(f"Signature valid: {is_valid}")
