use nucleic_acid_test;

drop table if exists manufacturer_detection_box;
drop table if exists manufacturer;

create table if not exists manufacturer(
    id varchar(50) not null primary key ,
    factory_name varchar(30) not null unique ,
    factory_prefix varchar(30) not null unique
)engine = innodb;

insert into manufacturer
values
(1,'小明生产厂','hello1'),
(2,'小红生产厂','hello2'),
(3,'小王生产厂','hello3'),
(4,'小飞生产厂','hello4'),
(5,'小静生产厂','hello5');

create table if not exists manufacturer_detection_box(
    id varchar(50) not null primary key ,
    factory_id varchar(50) not null,
    production_serial_number varchar(50),
    md5_result varchar(50),
    foreign key (factory_id) references manufacturer(id)
)engine = innodb;

insert into manufacturer_detection_box
values
(1,1,'',''),
(2,2,'',''),
(3,3,'',''),
(4,4,'',''),
(5,5,'','');
