import grpc
import codecs
import os
from time import sleep

import lib.rpc_pb2 as lnrpc
import lib.rpc_pb2_grpc as rpc_stub


# def check_lnd():
    # try:
    #     stub = get_stub()
    #     metadata = [('macaroon',get_macaroon())]
    #     response = stub.GetInfo(lnrpc.GetInfoRequest(),metadata=metadata)
    #     response.num_active_channels
    # except grpc._channel._InactiveRpcError:
    #     sleep(2)
    #     check_lnd()

class LndGRPC:
    def __init__(self):
        self.stub = self._get_stub()
        self.metadata = [('macaroon', self._get_macaroon())]

    def _get_stub(self):
        cert = open(os.path.expanduser('./lnd/tls.cert'), 'rb').read()
        creds = grpc.ssl_channel_credentials(cert)
        lnurl = "%s:%s"%(os.getenv('LND_IP'), os.getenv('LND_GRPC_PORT'))
        channel = grpc.secure_channel(lnurl, creds)
        stub = rpc_stub.LightningStub(channel)
        return stub
    
    def _get_macaroon(self):
        if(os.getenv("USE_REGTEST")):
            with open('./lnd/data/chain/bitcoin/regtest/admin.macaroon', 'rb') as f:
                macaroon_bytes = f.read()
                macaroon = codecs.encode(macaroon_bytes, 'hex')
        elif(os.getenv("USE_TESTNET")):
            with open('./lnd/data/chain/bitcoin/testnet/admin.macaroon', 'rb') as f:
                macaroon_bytes = f.read()
                macaroon = codecs.encode(macaroon_bytes, 'hex')
        else:
            with open('./lnd/data/chain/bitcoin/mainnet/admin.macaroon', 'rb') as f:
                macaroon_bytes = f.read()
                macaroon = codecs.encode(macaroon_bytes, 'hex')
        return macaroon

    # Returns the forwarding events of the last 24H
    def get_forwarding_events(self):
        response = self.stub.ForwardingHistory(lnrpc.ForwardingHistoryRequest(), metadata=self.metadata)        
        try:
            return str(len(response.forwarding_events))
        except:
            return "0"
