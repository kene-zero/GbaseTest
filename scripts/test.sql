-- 切换schema
set current_schaema = test;
select * from pg_proc where proname like '%sync_zhprs_custom %';

--创建表test1。
CREATE TABLE test1
(
  a1 smallint not null,
  a2 int not null,
  a3 bigint not null,
  a4 float not null,
  a5 double not null,
  a6 numeric not null,
  a7 varchar(5) not null
);

CREATE TABLE
--向表中插入记录失败。
insert into test1(a1,a2) values(123412342342314,3453453453434324);
ERROR:  smallint out of range
CONTEXT:  referenced column: a1
--查询表失败
select a1,a2 from test1 group by a1;
ERROR:  column "test1.a2" must appear in the GROUP BY clause or be used in an aggregate function
LINE 1: select a1,a2 from test1 group by a1;

--向表中插入记录成功。
set dolphin.sql_mode = '';
SET
insert into test1(a1,a2) values(123412342342314,3453453453434324);
WARNING:  invalid input syntax for numeric: ""
CONTEXT:  referenced column: a6
WARNING:  smallint out of range
CONTEXT:  referenced column: a1
WARNING:  integer out of range
CONTEXT:  referenced column: a2
INSERT 0 1
--查询表成功
select a1,a2 from test1 group by a1;
  a1   |     a2
-------+------------
 32767 | 2147483647
(1 row)

--删除表
DROP TABLE test1;
DROP TABLE




Declare
-- -Required Declaration
input message varchar2;
output msg varchar2;
Begin
l_con :=                UTL_TCP.open_connection (remote_host      => --ip address of plugin,
                                                 remote_port      => port number,
                                                 tx_timeout       => timeout
                                                 );
---once connected
a:=UTL_TCP.write_text (l_con, );
UTL_TCP.FLUSH (i_conn);
LOOP
 IF (UTL_TCP.available (i_conn) > 0)
               THEN
begin
UTL_TCP.read_text (i_conn,
                                        output msg,
                                        UTL_TCP.available (i_conn)
                                       );
End if;
exception
--exception
End loop;
Exception
----Catching exception
End;

-- 存储过程
CREATE OR REPLACE PROCEDURE  proc_job_rerun_bak(_IN_JOB_CTL_DT IN varchar(20),_IN_END_DATE in varchar(20),_OUT_STATE OUT varchar(2))
  SECURITY DEFINER
AS declare
declare _FLG BOOLEAN;
declare _JOB_CTL_DATE varchar(20);
declare _JOB_NEXT_DATE varchar(20);
BEGIN
  _OUT_STATE :=0;
  _FLG := _IN_JOB_CTL_DT < _IN_END_DATE;
  IF _IN_JOB_CTL_DT < _IN_END_DATE THEN
    _JOB_CTL_DATE := to _char(to_date(_IN_JOB_CTL_DT,'yyyy-mm-dd'),'yyyy-mm-dd');
    _JOB_NEXT_DATE := to_char(to_date(_JOB_CTL_DATE,'yyyy-mm-dd')+ INTERVAL '1 day','yyyy-mm-dd');

    UPDATE  job_ctl_dtl
    SET
      JOB_CTL_DT = TO_DATE(_JOB_NEXT_DATE,'yyyy-mm-dd'),
      JOB_CTL_STS_TP_ID = 'WAITING'
    where JOB_ID IN (
      select JOB_ID
      from job_metadata where JOB_BLNG_SYS = '1008'
      and case when JOB_FRQ ='MONTH'
        then SUBSTRING_INNER(TO_CHAR(TO_DATE(_IN_JOB_CTL_DT,'yyyyMMdd') + INTERVAL '1 DAY','yyyyMMdd'),7,2) = '01'
        else
          true
        end
    );
  _OUT_STATE :=1;
  end if;
  _OUT_STATE :=1;
COMMIT;
END;


-- create TABLE test ()
create user test1 with sysadmin createrole auditadmin poladmin password 'gbase;123';


create table test1(
id int,
name varchar(10),
sale_day int,
sale_month int,
sale_year int)distribute by replication TO group singnode1;
create table test2(
id int,
name varchar(10),
sale_day int,
sale_month int,
sale_year int)distribute by replication TO group singnode1;

insert into test1 values(1,'zhangsan',2,9,2008);
insert into test1 values(2,'zhangsan',2,8,2007);
insert into test1 values(1,'zhangsan',2,9,2009);
insert into test1 values(1,'zhangsan',20,1,2010);
insert into test1 values(1,'zhangsan',2,9,2022);

gsql -d postgres -p 5432 -c "copy test1 to stdout (format 'binary');" I gsgl -d potgres -p 5432 -c "copy test2 from stdin (format 'binary');"

insert into test2 SELECT * from test1;


\copy a from stdin;

create table tf2 (cl int, c2 int, c3 varchar(32), c4 varchar(32), c5 int) ;
create table tf3 (cl int, c2 int, c3 varchar(32), c4 varchar(32), c5 int) ;
gsql -d postgres -p 5432 -c "copy tf1 to stdout (format 'binary');" I gsgl -d potgres -p 5432 -c "copy tfl from stdin (format 'binary');"


create table tfl(cl int, c2 int, c3 varchar(32), c4 varchar(32) , c5 int) ;
insert into tfl values(5,400,'USA','New York',35000);
insert into tfl values(4,300,'China','Changsha',24000);
begin;
declare mycur cursor for select * from tfl order by cl desc for update;
fetch next from mycur ;
update tfl set c2-c2+1 where current of mycur ;
end;
select * from tfl;



COPY tpcds.ship_mode_t1 FROM '/home/omm/ds_ship_mode.dat' ;



create table test2(id int,doc jsonb
);--针对jsonb 插入部分值
insert into test2 values(1,'{"nickname": "gs", "tags": ["python", "golang", "db"]}')
insert into test2 values(2,'{"num":2,"nickname": "gs", "tags": ["python", "golang", "db"]}')

select  id,doc :: json->>'nickname' from test2
select * from test2 where  doc :: json->>'num'='2'

create extension zhparser;
CREATE TEXT SEARCH CONFIGURATION zh (PARSER = zhparser);
ALTER TEXT SEARCH CONFIGURATION zh ADD MAPPING FOR n,v,a,i,e,l,j WITH simple;
select to_tsvector('zh','十九大精神');


--创建name_age表
create table name_age(name jsonb,tsvector tsvector);
insert into name_age values ('{"nickname": "hello", "tags": ["java", "golang", "db"]}','Sleep deprivation curing depression');
insert into name_age values ('{"nickname": "中国台湾是中国的一部分", "tags": ["java", "golang", "db"]}','Sleep deprivation curing depression');

create index idx_name_index on name_age using gin(to_tsvector('zh', name));
SELECT name,to_tsvector('zh',name)FROM name_age where to_tsvector('zh',name) @@ to_tsquery('zh','golang')




create or replace function random_range(int4,int4)
returns int4
language SQL
as $$
select ($1+floor(($2-$1+1)*random()))::int4;
$$;
CREATE FUNCTION

create or replace function random_text_simple(length int4)
findb-# returns text
findb-# language PLPGSQL
findb-# as $$
 DECLARE
 possible_chars text:='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
 output text :='';
 i int4;
 pos int4;
 begin
 for i in 1..length loop
 pos :=random_range(1,length(possible_chars));
 output:=output||substr(possible_chars,pos,1);
 end loop;
 return output;
 end;
 $$;
CREATE FUNCTION
postgres@findb:\df
                              List of functions
 Schema |        Name        | Result data type | Argument data types | Type
--------+--------------------+------------------+---------------------+------
 public | random_range       | integer          | integer, integer    | func
 public | random_text_simple | text             | length integer      | func
(2 rows)
select random_text_simple(5);
 random_text_simple
--------------------
 GRWZ6
(1 row)
truncate table user_ini;
TRUNCATE TABLE


insert into user_ini(id,user_id,user_name) select r,round(random()*1000000),random_text_simple(6) from generate_series(1,1000000) as r ;
INSERT 0 1000000
create table tbl_user_search_json(id serial,user_info json);
CREATE TABLE
insert into tbl_user_search_json(user_info) select row_to_json(user_ini) from user_ini;
INSERT 0 1000000
postgres@findb:\timing on
Timing is on.
select * from tbl_user_search_json where to_tsvector('english',user_info)@@to_tsquery('ENGLISH','GUNTVU');
 id |                                         user_info
----+-------------------------------------------------------------------------------------------
  7 | {"id":7,"user_id":550209,"user_name":"GUNTVU","create_time":"2020-12-19T12:11:55.070116"}
(1 row)

Time: 2371.057 ms (00:02.371)

create index idx_tbl_user_search_json on tbl_user_search_json using gin(to_tsvector('english',user_info));
CREATE INDEX
Time: 15754.502 ms (00:15.755)
select * from tbl_user_search_json where to_tsvector('english',user_info)@@to_tsquery('ENGLISH','GUNTVU');
 id |                                         user_info
----+-------------------------------------------------------------------------------------------
  7 | {"id":7,"user_id":550209,"user_name":"GUNTVU","create_time":"2020-12-19T12:11:55.070116"}
(1 row)



create table t1(a int,b int);
insert into t1 VALUES(1,2);
insert into t1 VALUES(2,2);


--创建单分片
create node group singnode with(dn1) ;
-- 创建单分片表
create table job metadata（
job_id bigint primary key,
job_nm character varying(128) default NULL,
job_tp character varying(50) default NULL
)to group singnode ;


--创建表test1。
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);
INSERT INTO products (product_name, price) VALUES('Product A', 29.99),('Product B', 49.99),('Product C', 19.95);



CREATE TABLE employees (employee_id SERIAL PRIMARY KEY,first_name VARCHAR(50) NOT NULL,last_name VARCHAR(50) NOT NULL,department_id INT NOT NULL);

INSERT INTO employees (first_name, last_name, department_id) VALUES('John', 'Doe', 1),('Alice', 'Smith', 2),('Bob', 'Johnson', 1),('Eva', 'Williams', 3);

SELECT first_name, (SELECT MAX(department_id) FROM employees) AS max_value FROM employees;
SELECT first_name, (SELECT MIN(department_id) FROM employees) AS max_value FROM employees;
SELECT first_name, (SELECT SUM(department_id) FROM employees) AS max_value FROM employees;
SELECT first_name, (SELECT AVG(department_id) FROM employees) AS max_value FROM employees;
SELECT first_name, (SELECT count(department_id) FROM employees) AS max_value FROM employees;


SELECT * FROM employees WHERE department_id =
(SELECT department_id FROM employees GROUP BY department_id HAVING MAX(salary) =
(SELECT MAX(salary) FROM employees WHERE department_id = 1));
