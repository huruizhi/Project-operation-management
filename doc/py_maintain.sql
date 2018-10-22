SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `py_maintain_data_check_mabiao`
-- ----------------------------
DROP TABLE IF EXISTS `py_maintain_data_check_mabiao`;
CREATE TABLE `py_maintain_data_check_mabiao` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `table_name` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '表名',
  `column_name` varchar(500) COLLATE utf8_bin DEFAULT NULL COMMENT '字段名',
  `check_type` tinyint(4) DEFAULT NULL COMMENT '检查类型:\r\n            1.不能为空\r\n            2.范围检查\r\n            3.逻辑条件检查',
  `min_value` decimal(16,4) DEFAULT NULL COMMENT '范围最小值',
  `max_value` decimal(16,4) DEFAULT NULL COMMENT '范围最大值',
  `judging_condition` varchar(500) COLLATE utf8_bin DEFAULT NULL COMMENT '逻辑条件',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='基础数据质控检查码表';

-- ----------------------------
--  Table structure for `py_maintain_data_error_info`
-- ----------------------------
DROP TABLE IF EXISTS `py_maintain_data_error_info`;
CREATE TABLE `py_maintain_data_error_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `check_date` datetime DEFAULT NULL COMMENT '质控检查推送时间',
  `table_name` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '表名',
  `pri_name` varchar(150) COLLATE utf8_bin DEFAULT NULL COMMENT '主键名称',
  `pri_key` varchar(150) COLLATE utf8_bin DEFAULT NULL,
  `column_name` varchar(30) COLLATE utf8_bin DEFAULT NULL COMMENT '字段名',
  `error_desc` varchar(1000) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='基础数据质控检查错误数据表';

-- ----------------------------
--  Table structure for `py_maintain_module_list_info`
-- ----------------------------
DROP TABLE IF EXISTS `py_maintain_module_list_info`;
CREATE TABLE `py_maintain_module_list_info` (
  `project_id` int(11) NOT NULL COMMENT '项目id',
  `module_id` int(11) NOT NULL COMMENT '模块id',
  `module_name` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '模块名称',
  `content_path` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '域名',
  `svn_addr` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT 'SVN地址',
  `build_api` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '构建API',
  `port_no` varchar(30) COLLATE utf8_bin DEFAULT NULL COMMENT '端口号',
  `db_conn` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '数据库连接',
  `test_server` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '测试服务器',
  `docker` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT 'docker网络',
  `owner` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '责任人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `project_status` tinyint(4) DEFAULT NULL COMMENT '项目状态:\r\n            1.已创建项目\r\n            2.可部署\r\n            3.已部署\r\n            4.已在正式环境运行',
  `run_number` int(10) DEFAULT '1' COMMENT 'spring_boot启动个数-用于负载均衡(1-5)',
  `module_type` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`project_id`,`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='项目清单表';

-- ----------------------------
--  Table structure for `py_maintain_project_mabiao`
-- ----------------------------
DROP TABLE IF EXISTS `py_maintain_project_mabiao`;
CREATE TABLE `py_maintain_project_mabiao` (
  `project_id` int(11) NOT NULL COMMENT '项目id',
  `project_name` varchar(80) COLLATE utf8_bin DEFAULT NULL COMMENT '项目名称',
  `project_eng_name` varchar(80) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='项目码表';

-- ----------------------------
--  Table structure for `py_stock_2_1.py_stock_marketing_info_2_1_ts`
-- ----------------------------
DROP TABLE IF EXISTS `py_stock_2_1.py_stock_marketing_info_2_1_ts`;
CREATE TABLE `py_stock_2_1.py_stock_marketing_info_2_1_ts` (
  `concat(ticker,trading_date)` text COLLATE utf8_bin,
  `pri_name` text COLLATE utf8_bin,
  `check_date` datetime DEFAULT NULL,
  `table_name` text COLLATE utf8_bin,
  `column_name` text COLLATE utf8_bin,
  `error_desc` text COLLATE utf8_bin
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
--  Table structure for `py_user_base_info`
-- ----------------------------
DROP TABLE IF EXISTS `py_user_base_info`;
CREATE TABLE `py_user_base_info` (
  `user_id` varchar(30) COLLATE utf8_bin NOT NULL COMMENT '账号=用户所在银行英文简称+系统的自增ID',
  `user_pwd` varchar(128) COLLATE utf8_bin NOT NULL COMMENT '密码',
  `user_pwd_flag1` varchar(256) COLLATE utf8_bin NOT NULL COMMENT '密码特征值1',
  `usr_pwd_flag2` varchar(256) COLLATE utf8_bin NOT NULL COMMENT '密码特征值2',
  `user_ip` varchar(60) COLLATE utf8_bin DEFAULT NULL COMMENT 'IP地址属性',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '账号注册时间',
  `expiration_time` datetime DEFAULT NULL COMMENT '账号到期时间',
  `user_name` varchar(15) COLLATE utf8_bin DEFAULT NULL COMMENT '姓名',
  `bank_name` varchar(30) COLLATE utf8_bin DEFAULT NULL COMMENT '具体支行银行名称',
  `user_mobie_phone` varchar(15) COLLATE utf8_bin DEFAULT NULL COMMENT '联系电话(手机）',
  `user_phone` varchar(15) COLLATE utf8_bin DEFAULT NULL COMMENT '联系电话(座机）',
  `use_fax` varchar(15) COLLATE utf8_bin DEFAULT NULL COMMENT '传真',
  `user_qq` varchar(20) COLLATE utf8_bin DEFAULT NULL COMMENT 'QQ',
  `weixin` varchar(20) COLLATE utf8_bin DEFAULT NULL COMMENT '微信',
  `user_email` varchar(80) COLLATE utf8_bin DEFAULT NULL COMMENT '邮箱',
  `user_city` varchar(15) COLLATE utf8_bin DEFAULT NULL COMMENT '城市',
  `news_preferences` varchar(100) COLLATE utf8_bin DEFAULT NULL COMMENT '媒体偏好',
  `is_trial_accounts` tinyint(6) NOT NULL COMMENT '是否试用账号0否 1是',
  `online_counts` tinyint(6) NOT NULL DEFAULT '1' COMMENT '同时在线次数',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '用户状态\r\n            0. 正常\r\n            1  一级锁定状态\r\n            2.二级锁定状态\r\n            3.管理员锁定状态\r\n            ',
  `special_flag` tinyint(6) DEFAULT NULL COMMENT '特殊标签：9忽略IP的用户',
  `is_hide` tinyint(6) DEFAULT '0' COMMENT '是否公开个人信息',
  `law_is_read` tinyint(6) DEFAULT '0' COMMENT '法律声明是否已读0否1是',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
--  Table structure for `py_user_privilege`
-- ----------------------------
DROP TABLE IF EXISTS `py_user_privilege`;
CREATE TABLE `py_user_privilege` (
  `user_id` varchar(30) COLLATE utf8_bin NOT NULL COMMENT '账号',
  `menu_id` smallint(6) NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`user_id`,`menu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='用户权限表';

SET FOREIGN_KEY_CHECKS = 1;
