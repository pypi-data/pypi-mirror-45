#!/bin/bash


PROP_PATH="/opt/iParapheur/tomcat/shared/classes/alfresco-global.properties"

if [ -f "$PROP_PATH" ]
then
  while IFS='=' read -r key value
  do
    key=$(echo $key | tr '.' '_')
    eval "${key}"=\${"value"} 2> /dev/null
  done < "$PROP_PATH"
else
  echo "- LE FICHIER DE PROPRIETE $1 EST INTROUVABLE : FIN DU SCRIPT"
  exit 1
fi


## -- Des variables
alfresco="/etc/init.d/alfresco"
PATH_IP="/opt/iParapheur/tomcat/shared/classes/"
db_url=`echo "$db_url" | awk -F/ '{ print $3 }' | awk -F: '{ print $1 }'`
db_port=`echo "$db_url" | awk -F/ '{ print $3 }' | awk -F: '{ print $2 }'`
DATA_PATH="$dir_root/contentstore/"
if [ -z "$db_port" ]
then
  db_port="3306"
fi
mysql="-h $db_url -P $db_port -u $db_username -p$db_password"

## -- Quelques test
IF_FILE_EXIST ()
{
if [ ! -f $1 ]; then
  echo "- LE DOSSIER $1 N'EXISTE PAS"
  echo " -FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}


IF_DIR_EXIST ()
{
if [ ! -d $1 ]; then
  echo "LE DOSSIER $1 N'EXISE PAS"
  echo "- FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}

TEST_SERVICE ()
{
if ! which $1 >/dev/null; then
  echo "- LE SERVICE $1 N EXISTE PAS"
  echo "FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}


## -- ON LANCE LES TESTS
echo -e "\n ** PREREQUIS **\n"
IF_FILE_EXIST $alfresco
IF_DIR_EXIST $PATH_IP
IF_FILE_EXIST $PROP_PATH
TEST_SERVICE "mysql"
IF_DIR_EXIST $DATA_PATH


mysql $mysql -e 'exit' $db_name
if [ $? -ne 0 ]; then
    echo "- CONNEXION A LA BASE DE DONNEES IMPOSSIBLE"
    echo "- FIN DU SCRIPT"
    exit 1
fi
echo -e "\n- CONNEXION A LA BASE DE DONNEES => OK\n"


echo "DELIMITER //" > myproc.sql
echo "CREATE PROCEDURE count_files()" >> myproc.sql
echo "bEGIN" >> myproc.sql
echo "SELECT" >> myproc.sql
echo "  bureau.qname_localname AS Bureau_Name," >> myproc.sql
echo "  banette.qname_localname AS Bureau_Name," >> myproc.sql
echo "  COUNT(dossier.child_node_id) AS Dossiers_Count" >> myproc.sql
echo "FROM alf_child_assoc AS bureau" >> myproc.sql
echo "  JOIN alf_child_assoc AS banette ON bureau.child_node_id = banette.parent_node_id" >> myproc.sql
echo "          JOIN alf_child_assoc AS dossier ON dossier.parent_node_id = banette.child_node_id" >> myproc.sql
echo "WHERE bureau.parent_node_id = (" >> myproc.sql
echo "  SELECT child_node_id" >> myproc.sql
echo "  FROM alf_child_assoc" >> myproc.sql
echo "  WHERE child_node_name='parapheurs'" >> myproc.sql
echo "  LIMIT 1" >> myproc.sql
echo ")" >> myproc.sql
echo "AND banette.qname_localname IN ('retournes', 'a-archiver', 'a-traiter', 'en-preparation', 'en-retard', 'dossiers-delegues')" >> myproc.sql
echo "GROUP BY bureau.qname_localname, banette.qname_localname" >> myproc.sql
echo "HAVING Dossiers_Count >= 0;" >> myproc.sql
echo "END;" >> myproc.sql
echo "//" >> myproc.sql
echo "DELIMITER ;" >> myproc.sql




## -- ON injecte la procédure
mysql $mysql $db_name < myproc.sql >/dev/null 2>&1
mysql $mysql -e 'CALL count_files();' $db_name
exit 1

exit 0
