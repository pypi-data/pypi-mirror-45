# Ungleich dns cli tool

A python package to set reverse dns in ungleich vm.

## Usage

installing the package via pip (python3 required)

```angular2
python3 -m pip install ungleich-cli
```
after installed you can set the reverse dns by typing

```angular2
ungleich-cli dns --set-reverse <ip> --user <username> --token <token> --name mirror.example.com
```