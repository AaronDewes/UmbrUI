## UmbrUI (Umb-roo-eee)
### [Umbrel](https://github.com/getumbrel/umbrel) UI developed for 3.5" GPIO screens

- This is still very early stages 
- Intended to be run as part of the Umbrel App system (hence the docker-compose)

The goal is to be able to present the user with some helpful information such as: 
- IP/TOR address 
- QR Code to link to url
- Funds Status
- How many channels
- Forwards in the last 24hrs

Early doors figma: https://www.figma.com/file/nPWWBp3BCrX71FmxRNnj1M/UmbrUI?node-id=0%3A1

We can go the Raspiblitz route and add some touchscreen functionality but for now I think this should focus on presenting some basic data to allow the user to get up and running.

To run localy (within X / mac):
```
NOTPI=true python3 ui.py
```

On Pi:
```
python3 ui.py
```

Make sure to configure the RPC access before running that:

```
export LND_IP=10.0.0.9
export LND_GRPC_PORT=10009
export BITCOIN_IP=10.0.0.8
export BITCOIN_RPC_PORT=18443
export BITCOIN_P2P_PORT=18444
export BITCOIN_RPC_USER=umbrel
export BITCOIN_RPC_PASS=GzE-ZFH2yZL82R_KWtY8kPxcb62e8eibQsGB0ag9Ip8=
```

Replace these vaulues with your actual data.

In addition, you can set `USE_REGTEST` or `USE_TESTNET` to use these networks.

Make sure to copy your lnd folder to this directory befor starting.

And you'll need to login to the dashboard once.