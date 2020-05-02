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

@click.group()
def cli():
    """Shotty manages snapshots"""
        
#Funcion que nos lista las instancias de una cuenta en AWS
@cli.group("instances")
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
        try:
            instance.stop()
        except botocore.exceptions.ClientError as e:
            print(" Cloud not stop {0}".format(instance.id) + str(e))
            continue
    return

#Funcion que inicia las instancias de una cuenta AWS
@instances.command('start')
@click.option('--project', default=None, help='Only instances for project')
def start_instance(project):
    "Start EC2 instances"
    
    instances = filter_instances(project)

    for instance in instances:
        print ("Starting {0}...".format(instance.id))
        try:
            instance.start()
        except botocore.exceptions.ClientError as e:
            print(" Cloud not start {0}".format(instance.id) + str(e))
            continue
    return

@instances.command('snapshot', help="Create snapshots of all volumes")
@click.option('--project', default=None, help='Only instances for project')
def create_snapshots(project):
    "Create snapshots for EC2 instances"
    
    instances = filter_instances(project)

    for instance in instances:
        print("Stopping {0}...".format(instance.id))
        instance.stop()
        instance.wait_until_stopped()
        for volume in instance.volumes.all():
            print("Creating snapshot of {0}".format(volume.id))
            volume.create_snapshot(Description="Created by SnapshotAlyzer")
        
        print("Starting {0}...".format(instance.id))

        instance.start()
        instance.wait_until_running()
    
    print("Job's done!")

    return

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command("list")
@click.option('--project', default=None,
    help='Only snapshots for project (tag Project:<name>)')

def list_snapshots(project):
    "list EC2 snapshots"
    
    instances = filter_instances(project)

    for instance in instances:
        for volume in instance.volumes.all():
            for snapshot in volume.snapshots.all():
                print(", ".join((
                    snapshot.id,
                    volume.id,
                    instance.id,
                    snapshot.state,
                    snapshot.progress,
                    snapshot.start_time.strftime("%c")
                )))
    return

#@click.option()
@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command("list")
@click.option('--project', default=None,
    help='Only intances for project (tag Project:<name>)')

def list_volumes(project):
    "list EC2 volumes"
    
    instances = filter_instances(project)
    
    for instance in instances:
        for volume in instance.volumes.all():
            print(', '.join((
                volume.id,
                instance.id,
                volume.state,
                str(volume.size) + "GiB",
                volume.encrypted and "Encryted" or "Not Encryted"
                )))
    return 


   
if __name__ == '__main__':
    cli()