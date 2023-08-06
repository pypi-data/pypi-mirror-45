import requests
import click


@click.command()
@click.argument('dns', required=False)
@click.option('--set-reverse', help='REQUIRED: IPv6 Address of your VM', required=True)
@click.option('--user', help='Your ungleich username', required=True)
@click.option('--token', help='REQUIRED: Your ungleich 6 digit OTP generated token', type=int)
@click.option('--name', help='REQUIRED: Hostname', required=True)
def cli(dns, set_reverse, user, token, name):
    """This script set the reverse dns for your VM

    Example Usage:

    ungleich-cli dns --set-reverse <ip> --user <username> --token <token> --name mirror.example.com

    """
    r = requests.post('https://ungleich.ch/dns/reverse/', json={'username': user, 'token': token, 'ipaddress': set_reverse, 'name': name})
    return click.echo(r.text)
