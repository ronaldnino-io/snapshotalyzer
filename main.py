#
#Alyzer script tiene como fin automatizar la interacción con instancias ec2
#Autor: Ronald Niño
#

#Importamos el kit de desarrollo de AWS
import boto3
import sys
import click

 #Iniciamos una sesión con una cuenta de AWS
session =  boto3.Session(profile_name='shotty')

#Nos conectamos al servicio de aec2
ec2 =  session.resource('ec2')

#Funcion que nos lista las instancias de una cuenta en AWS
@click.command()
def list_instances():
    "list EC2 instances"
    for instance in ec2.instances.all():
        print(', '.join((
            instance.id,
            instance.instance_type,
            instance.placement['AvailabilityZone'],
            instance.state['Name'],
            instance.public_dns_name)))
    return        

   
if __name__ == '__main__':
    list_instances()