Use mydata;
show tables;
show databases;
select * from myapp_userinfo ;
DELETE FROM myapp_userinfo;
TRUNCATE TABLE myapp_userinfo;
delete  from myapp_userinfo where id=4;
alter table myapp_userinfo drop  column id;
ALTER TABLE myapp_userinfo ADD ID INT AUTO_INCREMENT PRIMARY KEY FIRST;
UPDATE myapp_userinfo
SET gender = '男'
WHERE id = 3;
select * from myapp_userinfo where id=4;
select * from myapp_personalphoto ;