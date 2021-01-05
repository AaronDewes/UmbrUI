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

We can go the Raspiblitz route and add some touchscreen functionality but for now I think this should focus on presenting some basic data to allow the user to get up and running.

To run localy (within X / mac):
```
NOTPI=true python3 ui.py
```

On Pi:
```
python3 ui.py
```

