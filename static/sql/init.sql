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

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `open_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '微信ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '名称',
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '电话',
  `id_card` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '身份证',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (1, 'wx_hahaha', 'lin', '15950562146', '320125200206013610');
INSERT INTO `sys_user` VALUES (2, 'wx_imtheking', 'dyh', '18651831776', '320125199710273610');
INSERT INTO `sys_user` VALUES (4, 'wx_imtheQuess', 'hanjin', '18651831776', '320125199710273610');

DROP TABLE IF EXISTS `sys_event_detect`;
CREATE TABLE `sys_event_detect`  (
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `test_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '检测结果',
  `test_result` binary(1) NOT NULL COMMENT '是否通过'
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_event_detect
-- ----------------------------
INSERT INTO `sys_event_detect` VALUES (1, '2022-10-04 13:19:11', 0x31);
INSERT INTO `sys_event_detect` VALUES (1, '2022-10-04 14:08:05', 0x30);