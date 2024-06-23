CREATE DATABASE IF NOT EXISTS `fazbot`;
CREATE DATABASE IF NOT EXISTS `fazbot_test`;
CREATE DATABASE IF NOT EXISTS `wynndb`;
CREATE DATABASE IF NOT EXISTS `wynndb_test`;

CREATE USER IF NOT EXISTS 'fazbot'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON `fazbot`.* TO 'fazbot'@'%';
GRANT ALL PRIVILEGES ON `fazbot_test`.* TO 'fazbot'@'%';
GRANT ALL PRIVILEGES ON `wynndb`.* TO 'fazbot'@'%';
GRANT ALL PRIVILEGES ON `wynndb_test`.* TO 'fazbot'@'%';
FLUSH PRIVILEGES;
