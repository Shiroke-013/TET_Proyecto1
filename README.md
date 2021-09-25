# TET_Proyecto1
## Autores: Catalina López Roldán y Andres Dario Chaves
## Descripción
El proyecto 1 tiene como objetivo el almacenar registros de tipo <key, value> que seran enviados desde diversos clientes. Se a seleccionado un arquitectura Cliente/Servidor, además se usaran recursos como lo son RDS wn aws para aplicar replicación y tolerancia a fallos, ya que este recurso crea una replica de la base de datos master de donde se podran leer datos y si es necesario restaurarlos en caso de perdida de información. La "key" del registro puede ser cualquier tipo de string al igual que el "value".

## Instalación
Se debe instanciar tres o mas instancias EC2 en AWS, una de esta sera el servidor y las otras los clientes que se van a guardar los registros en la base de datos.
Estas instancias deben tener dos grupos de seguridad (SG) diferentes, el SG del Servidor debe tener el puerto seleccionado para TCP (ej. 1313), abierto para cualquir IP, ademas del puerto de Aurora/Mysql (ej. 3306). Por otro lado el puesto TCP del SG de los clientes, que va con el mismo numero, debe estar solo abierto para la IP publica del Servidor. Hay que tener en cuenta que la instancia del Servidor debe llevar una IP elastica asociada.

Todas las instancias deben contra con python 3, ademas de git y un edito de texto de preferencia, se pueden instalar con los siguientes comandos:
<pre><code> $ sudo yum install git
 $ sudo yum install emacs 
 $ sudo yum install python3
</code></pre>

Ademas se debe installar la biblioteca de pymysql con el siguiente comando:
<pre><code> $ python3 -m pip install pymysql
</code></pre>

Se planteo una arquitectura del proyecto la cual de ve así:
[Arquitectura]!(https://github.com/Shiroke-013/TET_Proyecto1/blob/main/Arquitectura_Proyecto1.drawio.png)

## Ejecución
Primero es necesario crear una base de datos en el recurso RDS de AWS, este debe llevar las siguientes caracteristicas: debe ser Aurora compatible con MySQL, debe estar abierta a conexiones de otras instancias EC2, el grupo de seguridad debe estar abierto a todo trafico por el puerto 3306, debe recordar que usurario y contraseña se ingresa en la configuración.
Luego, para ejecutar el programa se debe acceder a las instancias por medio de ssh y clonar el repositorio.
Luego de verificar esto se debe correr en la instancia servidor el archivo Server.py de la siguiente manera:
<pre><code> $ python3 Server.py 0.0.0.0 [PUERTO] [HOST] [USUARIO] [CONTRASEÑA] [NOMBRE_DB]
</code></pre>
Luego de tener el servidor corriendo se puede poner a correr los clientes que se desee de la siente manera:
<pre><code> $ python3 Client1.py [PUBLIC_IP_SERVER] [PUERTO]
</code></pre>
PUBLIC_IP_SERVER: La IP publica de la instancia que funciona como servidor. <br />
PUERTO: El puerto previamente seleccionado y abierto para TCP. <br />
HOST: EndPoint de la base de datos master. <br />
USUARIO: Usuario de acceso a la base de datos master. <br />
CONTRASEÑA: Contraseña de acceso a la base de datos master. <br />
NOMBRE_DB: El nombre de la base de datos a la que se hara la conexión, ya que la tabla dentro de la base de datos llevara el mismo nombre.

# Referencias
- https://www.geeksforgeeks.org/distributed-database-system/
- https://es.wikipedia.org/wiki/Write_Once_Read_Many
- https://es.wikipedia.org/wiki/Replicaci%C3%B3n_(inform%C3%A1tica)
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html
