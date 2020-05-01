#
#Alyzer script tiene como fin automatizar la interacción con instancias ec2
#Autor: Ronald Niño
#

#Importamos el kit de desarrollo de AWS
import boto3

if __name__ == '__main__':
    #Iniciamos una sesión con una cuenta de AWS
    session =  boto3.Session(profile_name='shotty')

    #Nos conectamos al servicio de aec2
    ec2 =  session.resource('ec2')

    #Visualizamos todas las instancias que tenemo en ec2
    for instance in ec2.instances.all():
        print(instance)
