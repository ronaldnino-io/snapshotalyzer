#
#Alyzer script tiene como fin automatizar la interacción con instancias ec2
#Autor: Ronald Niño
#

#Importamos el kit de desarrollo de AWS
import boto3
#Importamos el paque que nos ayudara a la implementacion de un CLI
import click

#Iniciamos una sesión con una cuenta de AWS
session =  boto3.Session(profile_name='shotty')

#Nos conectamos al servicio de aec2
ec2 =  session.resource('ec2')

#Funcion que nos devuelve una lista de instancias filtrada por el tag project
def filter_instances(project):
    
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

#Funcion que nos lista las instancias de una cuenta en AWS
@click.group()
def instances():
    """Commands for instances"""

@instances.command("list")
@click.option('--project', default=None,
    help='Only intances for project (tag Project:<name>)')
def list_instances(project):
    "list EC2 instances"
    
    instances = filter_instances(project)
    
    for instance in instances:
        tags = {t['Key']: t['Value'] for t  in instance.tags or []}
        print(', '.join((
            instance.id,
            instance.instance_type,
            instance.placement['AvailabilityZone'],
            instance.state['Name'],
            instance.public_dns_name,
            tags.get('Project', '<no project>'
            
            ))))
    return        

#Funcion que pausa las instancias de una cuenta AWS
@instances.command('stop')
@click.option('--project', default=None, help='Only instances for project')
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for instance in instances:
        print ("Stopping {0}...".format(instance.id))
        instance.stop()
    return

#Funcion que inicia las instancias de una cuenta AWS
@instances.command('start')
@click.option('--project', default=None, help='Only instances for project')
def stop_instances(project):
    "Start EC2 instances"
    
    instances = filter_instances(project)

    for instance in instances:
        print ("Starting {0}...".format(instance.id))
        instance.start()
    return


   
if __name__ == '__main__':
    instances()