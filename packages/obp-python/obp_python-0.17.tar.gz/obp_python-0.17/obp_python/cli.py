import click
import json
import os
from .auth_direct_login import getAuthToken
from .init import (init_config_dir, set_obp_api_host, set_obp_username, 
                  set_obp_password, set_obp_consumer_key, set_obp_auth_token,
                  set_obp_user_id, get_config)
from .sandboxImport import sandboxImport
from .getUserId import getUserId
from .addRole import addRole
from .getUserId import getUserId

@click.group()
def cli():
  pass

@cli.command(help="Bulk import sandbox data from json input")
@click.option('--input', type=click.File('rb'), required=False, help="Import from file")
@click.option('--example', required=False, is_flag=True, 
              help="Auto import very small example dataset")
def sandboximport(input=None, example=False):
  if input is None and example is False:
    click.echo("Invalid option. See obp sandboximport --help", err=True)
    exit(-1)
  if example: #load example import 
    input = open(os.path.join(os.path.dirname(__file__), '../example_import.json'))
  req = sandboxImport(src=input)
  if example:
    input.close()
  if req.status_code == 201 or req.status_code == 200:
    click.echo("Sandbox import complete")
  else:
    exit(req.text)


@cli.command(help="Initalize connection to your Open Bank Project instance")
def init():
  init_config_dir()
  OBP_API_HOST = click.prompt("Please enter your API_HOST: ", 
                              default=get_config("OBP_API_HOST",
                              default="http://127.0.0.1:8080",
                              allow_stdin=False))
  set_obp_api_host(OBP_API_HOST)
  OBP_USERNAME = click.prompt("Please enter your username: ",
                              default=get_config("OBP_USERNAME",
                              allow_stdin=False))
  set_obp_username(OBP_USERNAME)
  OBP_PASSWORD = click.prompt("Please enter your password: ", hide_input=True,
                              confirmation_prompt=True)
  set_obp_password(OBP_PASSWORD)
  
  click.echo("... generating direct login token")
  if get_config("OBP_CONSUMER_KEY", allow_stdin=False) is False:
    click.echo("Consumer key needed to generate a DirectLogin token")
    click.confirm("Do you have a consumer key?")
    if click.confirm("Would you like to generate one?", abort=True):
      exit("Not implemented. Visit {}, login, click \"Get an api key\" "
           "and register a consumer. This will give you a consumer key"
           " which you can use here.".format(OBP_API_HOST))
  else:
    OBP_CONSUMER_KEY = click.prompt("Please enter your OBP_CONSUMER_KEY: ",
                                    default=get_config("OBP_CONSUMER_KEY",
                                    allow_stdin=False))
    set_obp_consumer_key(OBP_CONSUMER_KEY)
    
  req = getAuthToken()
  if req.status_code == 201 or req.status_code == 200:
    authToken = json.loads(req.text)['token']
    set_obp_auth_token(authToken)
    # Get & set user id
    req = getUserId()
    if req.status_code == 201 or req.status_code == 200:
      set_obp_user_id(json.loads(req.text)['user_id']) 
    else:
      click.echo("Unable to get your user_id")
      exit(req.text)
  else:
    exit(req.text)

  click.echo("Init complete")

@cli.command(help="Get your DirectLogin token")
def getauth():
  authToken = getAuthToken()
  print(json.loads(authToken.text))

@cli.command(help="Get your user info")
def getuser():
  req = getUserId()
  if req.status_code == 201 or req.status_code == 200:
    click.echo(req.text)
  else:
    exit(req.text)

@cli.command(help="Get your user id")
def getuserid():
  req = getUserId()
  if req.status_code == 201 or req.status_code == 200:
    user_id = json.loads(req.text)['user_id']
    click.echo({'user_id': user_id})
  else:
    exit(req.text)

@cli.command(help="Add a role for current user")
@click.option('--role-name', required=True)
def addrole(role_name):
  req = addRole(role=role_name, require_bank_id=False)
  if req.status_code == 201 or req.status_code == 200:
    click.echo(req.text)
  else:
    exit(req.text)
