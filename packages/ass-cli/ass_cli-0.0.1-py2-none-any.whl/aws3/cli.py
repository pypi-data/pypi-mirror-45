from . import __version__
import click


INTERACTIVE_INIT_HELP = 'Start an interactive session to compose config file'


@click.version_option(__version__, message='%(version)s')
@click.group()
def main():
    ''' AWS-Serverless-Stack CLI. '''
    pass


@main.command('init')
@click.option('--interactive', '-i', is_flag=True, help=INTERACTIVE_INIT_HELP)
def init(interactive):
    ''' Initialize a project directory for AWS-Serverless-Stack. '''
    click.echo("Welcome to ASS")
