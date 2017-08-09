/*
Navicat MySQL Data Transfer

Source Server         : NSlab
Source Server Version : 50554
Source Host           : 172.26.253.3:3306
Source Database       : malicious_domain_sys

Target Server Type    : MYSQL
Target Server Version : 50554
File Encoding         : 65001

Date: 2017-05-28 19:53:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for domain_index
-- ----------------------------
DROP TABLE IF EXISTS `domain_index`;
CREATE TABLE `domain_index` (
  `ID` bigint(20) NOT NULL COMMENT '域名HASH ID',
  `domain` varchar(255) NOT NULL COMMENT '域名',
  `whois_flag` tinyint(2) NOT NULL DEFAULT '-99' COMMENT 'whois信息完整性标志',
  `locate_flag` int(11) NOT NULL DEFAULT '-100' COMMENT '地理位置信息完整性标志',
  `other_info_flag` int(6) NOT NULL DEFAULT '-100' COMMENT '其他信息完整性标志',
  `malicious_info_flag` int(6) NOT NULL DEFAULT '-100' COMMENT '恶意信息完整性标志',
  `funnel_level` int(6) NOT NULL DEFAULT '-100' COMMENT '数据筛选级别',
  `judge_flag` tinyint(2) NOT NULL DEFAULT '-10' COMMENT '域名类型判断结果',
  `judge_score` tinyint(3) NOT NULL DEFAULT '-100',
  `source` tinyint(2) NOT NULL DEFAULT '-10' COMMENT '域名来源',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`ID`),
  KEY `ind_domain` (`domain`) USING BTREE COMMENT '域名索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for info_reverse_search
-- ----------------------------
DROP TABLE IF EXISTS `info_reverse_search`;
CREATE TABLE `info_reverse_search` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `info` varchar(255) NOT NULL DEFAULT '' COMMENT '反查信息',
  `info_type` tinyint(2) NOT NULL DEFAULT '-10' COMMENT '反差信息类型',
  `done` tinyint(1) NOT NULL DEFAULT '0' COMMENT '此条反查完成标志',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'CURRENT_TIMESTAMP',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_info` (`info`(64)) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=96117 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for ip_history
-- ----------------------------
DROP TABLE IF EXISTS `ip_history`;
CREATE TABLE `ip_history` (
  `ID` bigint(20) NOT NULL COMMENT 'HASH_ID',
  `IP` varchar(16) NOT NULL DEFAULT '' COMMENT 'ip记录字符串',
  `record_time` datetime DEFAULT NULL COMMENT 'ip记录获取时间',
  KEY `ind_ID` (`ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for ip_history1
-- ----------------------------
DROP TABLE IF EXISTS `ip_history1`;
CREATE TABLE `ip_history1` (
  `ID` bigint(20) NOT NULL COMMENT 'HASH_ID',
  `IP` varchar(255) NOT NULL DEFAULT '' COMMENT 'ip记录字符串',
  `record_time` datetime DEFAULT NULL COMMENT 'ip记录获取时间',
  KEY `ind_ID` (`ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for locate
-- ----------------------------
DROP TABLE IF EXISTS `locate`;
CREATE TABLE `locate` (
  `ID` bigint(20) NOT NULL COMMENT 'HASH_ID',
  `flag` int(11) NOT NULL DEFAULT '-10' COMMENT '标记位',
  `country` varchar(32) NOT NULL DEFAULT '' COMMENT '国家',
  `country_code` varchar(8) NOT NULL DEFAULT '' COMMENT '国家码',
  `province` varchar(32) NOT NULL DEFAULT '' COMMENT '省/州/自治区',
  `city` varchar(32) NOT NULL DEFAULT '' COMMENT '市/乡镇',
  `postal_code` varchar(16) NOT NULL DEFAULT '' COMMENT '邮编',
  `street` varchar(64) NOT NULL DEFAULT '' COMMENT '街道',
  `phone` varchar(32) NOT NULL DEFAULT '',
  `reg_whois_province` varchar(32) NOT NULL DEFAULT '' COMMENT 'whois省',
  `reg_whois_city` varchar(32) NOT NULL DEFAULT '' COMMENT 'whois市',
  `reg_phone_province` varchar(32) NOT NULL DEFAULT '' COMMENT 'whois电话 省',
  `reg_phone_city` varchar(32) NOT NULL DEFAULT '' COMMENT 'whois电话 市',
  `reg_postal_province` varchar(32) NOT NULL DEFAULT '' COMMENT 'whois右边 省',
  `reg_postal_city` varchar(32) NOT NULL DEFAULT '' COMMENT 'whois邮编 市',
  `reg_postal_county` varchar(32) NOT NULL DEFAULT '' COMMENT 'whois邮编 国',
  `IP` varchar(255) NOT NULL DEFAULT '' COMMENT 'IP',
  `ICP` varchar(64) NOT NULL DEFAULT '' COMMENT 'ICP',
  `ICP_province` varchar(32) NOT NULL DEFAULT '' COMMENT 'ICP 省',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `IP_info` varchar(255) NOT NULL DEFAULT '' COMMENT 'IP解析信息',
  `cmp` int(11) NOT NULL DEFAULT '0' COMMENT '省相同数;市相同数',
  `cmpinfo` varchar(32) NOT NULL DEFAULT '' COMMENT '省相同数;电话(省);whois(省);邮编(省);IP(省);ICP(省);市相同数;电话(市);whois(市);邮编(市);IP(市)',
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_domain_index_ID_locate` FOREIGN KEY (`ID`) REFERENCES `domain_index` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for malicious_info
-- ----------------------------
DROP TABLE IF EXISTS `malicious_info`;
CREATE TABLE `malicious_info` (
  `ID` bigint(20) NOT NULL COMMENT 'HASH_ID',
  `flag` int(5) NOT NULL DEFAULT '0' COMMENT '标记位',
  `available` tinyint(2) NOT NULL DEFAULT '-10' COMMENT '可访问情况',
  `HTTPcode` int(6) NOT NULL DEFAULT '0' COMMENT '网站状态',
  `title` varchar(200) NOT NULL DEFAULT '' COMMENT '对应类型主题关键词',
  `judge_grade` tinyint(2) NOT NULL DEFAULT '0' COMMENT '评级可能性',
  `key_word` varchar(80) NOT NULL COMMENT '网站tfidf前五关键词',
  `malicious_keywords` varchar(200) NOT NULL COMMENT '对应类型恶意主题关键词',
  `influence` int(8) NOT NULL DEFAULT '-100' COMMENT '影响力',
  `influence_last_update` varchar(12) DEFAULT NULL COMMENT '影响力指数上次更新时间',
  `IP` varchar(255) NOT NULL DEFAULT '' COMMENT 'ip记录字符串',
  `IP_detect_time` datetime DEFAULT NULL COMMENT 'ip探测时间',
  `malicious_link` text NOT NULL COMMENT '恶意外链',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录插入时间',
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_domain_index_ID_malicious` FOREIGN KEY (`ID`) REFERENCES `domain_index` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for malicious_link
-- ----------------------------
DROP TABLE IF EXISTS `malicious_link`;
CREATE TABLE `malicious_link` (
  `url_id` bigint(20) NOT NULL COMMENT '恶意URL HASH值',
  `url` varchar(255) CHARACTER SET utf8mb4 NOT NULL DEFAULT '' COMMENT 'url',
  `url_domain` varchar(255) DEFAULT '' COMMENT '恶意url的域名，以便于同一域名不同路径时的处理情况',
  `type` tinyint(2) NOT NULL DEFAULT '0' COMMENT '恶意URL类型, 赌博 1， 色情 2',
  `level` tinyint(4) NOT NULL DEFAULT '-100' COMMENT '恶意URL等级',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`url_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for malicious_type
-- ----------------------------
DROP TABLE IF EXISTS `malicious_type`;
CREATE TABLE `malicious_type` (
  `id` int(10) unsigned NOT NULL COMMENT '恶意类型的符号',
  `type` varchar(64) NOT NULL DEFAULT '' COMMENT '根据恶意类型标号银蛇的恶意域名类型（如，1--赌博）',
  `tend_avg` text NOT NULL COMMENT '恶意类型平均趋势（存储逗号分隔的30个数据代表30天的热度）',
  `start_date` varchar(12) NOT NULL DEFAULT '' COMMENT 'tend_avg起点的时间',
  `end_date` varchar(12) NOT NULL DEFAULT '' COMMENT 'tend_avg终点的时间',
  `record_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'CURRENT_TIMESTAMP',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for other_info
-- ----------------------------
DROP TABLE IF EXISTS `other_info`;
CREATE TABLE `other_info` (
  `ID` bigint(20) NOT NULL COMMENT 'HASH_ID',
  `flag` tinyint(2) NOT NULL DEFAULT '-10' COMMENT '标记位',
  `Alex` varchar(255) NOT NULL DEFAULT '' COMMENT 'Alex排名',
  `Alex_last_update` date DEFAULT NULL COMMENT 'Alex排名上次更新时间',
  `web_judge_result` tinyint(4) NOT NULL DEFAULT '-100' COMMENT '权威网站检测结果',
  `appears_location` varchar(255) NOT NULL DEFAULT '暂无' COMMENT '域名在互联网上的出现位置',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录插入时间',
  PRIMARY KEY (`ID`),
  CONSTRAINT `tri_domain_index_ID_info` FOREIGN KEY (`ID`) REFERENCES `domain_index` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for reg_info_black_lists
-- ----------------------------
DROP TABLE IF EXISTS `reg_info_black_lists`;
CREATE TABLE `reg_info_black_lists` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `flag` tinyint(4) NOT NULL DEFAULT '-100' COMMENT '标志位(备用)',
  `info` varchar(255) NOT NULL DEFAULT '' COMMENT '恶意信息',
  `type` tinyint(4) NOT NULL DEFAULT '-100' COMMENT '恶意信息类型',
  `relation` varchar(255) NOT NULL DEFAULT '' COMMENT '与其他信息关联关系',
  `malicious_count` int(11) NOT NULL DEFAULT '-1' COMMENT '信息注册恶意域名趋势',
  `domain_count` int(11) NOT NULL COMMENT '信息注册总域名数',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_info` (`info`(32)) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14566 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for whois
-- ----------------------------
DROP TABLE IF EXISTS `whois`;
CREATE TABLE `whois` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `flag` tinyint(2) NOT NULL DEFAULT '-99' COMMENT '标记位',
  `domain` varchar(255) NOT NULL COMMENT '域名',
  `tld` varchar(32) NOT NULL DEFAULT '' COMMENT '顶级域',
  `domain_status` text COMMENT '域名状态值',
  `sponsoring_registrar` varchar(255) NOT NULL DEFAULT '' COMMENT '注册商',
  `top_whois_server` varchar(255) NOT NULL DEFAULT '' COMMENT '一级whois服务器',
  `sec_whois_server` varchar(255) NOT NULL DEFAULT '' COMMENT '二级whois服务器',
  `reg_name` varchar(255) NOT NULL DEFAULT '' COMMENT '注册者',
  `reg_phone` varchar(255) NOT NULL DEFAULT '' COMMENT '注册人电话',
  `reg_email` varchar(255) NOT NULL DEFAULT '' COMMENT '注册人邮箱',
  `org_name` varchar(255) NOT NULL DEFAULT '' COMMENT '注册公司',
  `name_server` text COMMENT '名称服务器',
  `creation_date` varchar(255) NOT NULL COMMENT 'whois记录创建时间',
  `expiration_date` varchar(255) NOT NULL DEFAULT '' COMMENT '域名过期时间',
  `updated_date` varchar(255) NOT NULL DEFAULT '' COMMENT 'whois记录更新时间',
  `details` text COMMENT '原始whois数据',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录插入时间',
  PRIMARY KEY (`ID`),
  KEY `ind_reg_name` (`reg_name`(32)) USING BTREE,
  KEY `ind_reg_phone` (`reg_phone`(15)) USING BTREE,
  KEY `ind_reg_email` (`reg_email`(32)) USING BTREE,
  KEY `flag` (`flag`),
  CONSTRAINT `fk_domain_index_ID_whois` FOREIGN KEY (`ID`) REFERENCES `domain_index` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9223150020710586480 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for whois_proxy
-- ----------------------------
DROP TABLE IF EXISTS `whois_proxy`;
CREATE TABLE `whois_proxy` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `proxy_ip` varchar(45) NOT NULL DEFAULT '' COMMENT '代理ip',
  `proxy_port` smallint(45) NOT NULL DEFAULT '8088' COMMENT '代理端口',
  `proxy_mode` varchar(11) NOT NULL DEFAULT '' COMMENT 'socks模式',
  `whois_ip` varchar(45) NOT NULL DEFAULT '' COMMENT '针对whoisIP',
  `speed` tinyint(4) NOT NULL DEFAULT '0' COMMENT '代理速度',
  `message` varchar(255) NOT NULL DEFAULT '' COMMENT '代理内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for whois_srvip
-- ----------------------------
DROP TABLE IF EXISTS `whois_srvip`;
CREATE TABLE `whois_srvip` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `svr_name` varchar(255) DEFAULT NULL COMMENT 'whois服务器地址',
  `ip` varchar(255) DEFAULT '' COMMENT 'whois服务器ip',
  `level` int(10) DEFAULT NULL COMMENT 'whois服务器级别',
  `rrt` varchar(255) DEFAULT NULL COMMENT 'RRT',
  `port_available` varchar(255) DEFAULT NULL COMMENT '端口可用性',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1817 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for whois_tld_addr
-- ----------------------------
DROP TABLE IF EXISTS `whois_tld_addr`;
CREATE TABLE `whois_tld_addr` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `TLD` varchar(255) NOT NULL DEFAULT '' COMMENT '顶级域',
  `Punycode` varchar(255) NOT NULL DEFAULT '' COMMENT 'puny码',
  `Type` varchar(255) NOT NULL DEFAULT '' COMMENT '类型',
  `whois_addr` varchar(255) NOT NULL DEFAULT '' COMMENT 'whois服务器',
  `SponsoringOrganization` varchar(255) NOT NULL DEFAULT '' COMMENT '注册商',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `TLD_UNIQUE` (`TLD`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=1567 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for whowas
-- ----------------------------
DROP TABLE IF EXISTS `whowas`;
CREATE TABLE `whowas` (
  `ID` bigint(20) NOT NULL COMMENT 'domain HASH',
  `flag` tinyint(2) NOT NULL DEFAULT '-10' COMMENT '标记位',
  `domain` varchar(255) NOT NULL COMMENT '域名',
  `tld` varchar(32) NOT NULL DEFAULT '' COMMENT '顶级域',
  `domain_status` text COMMENT '域名状态值',
  `sponsoring_registrar` varchar(255) NOT NULL DEFAULT '' COMMENT '注册商',
  `top_whois_server` varchar(255) NOT NULL DEFAULT '' COMMENT '一级whois服务器',
  `sec_whois_server` varchar(255) NOT NULL DEFAULT '' COMMENT '二级whois服务器',
  `reg_name` varchar(255) NOT NULL DEFAULT '' COMMENT '注册者',
  `reg_phone` varchar(255) NOT NULL DEFAULT '' COMMENT '注册人电话',
  `reg_email` varchar(255) NOT NULL DEFAULT '' COMMENT '注册人邮箱',
  `org_name` varchar(255) NOT NULL DEFAULT '' COMMENT '注册公司',
  `name_server` text COMMENT '名称服务器',
  `creation_date` varchar(255) NOT NULL COMMENT 'whois记录创建时间',
  `expiration_date` varchar(255) NOT NULL DEFAULT '' COMMENT '域名过期时间',
  `updated_date` varchar(255) NOT NULL DEFAULT '' COMMENT 'whois记录更新时间',
  `details` text COMMENT '原始whois数据',
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录插入时间',
  KEY `ind_reg_name` (`reg_name`(32)) USING BTREE,
  KEY `ind_reg_phone` (`reg_phone`(15)) USING BTREE,
  KEY `ind_reg_email` (`reg_email`(32)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
DROP TRIGGER IF EXISTS `tri_locate_flag_insert`;
DELIMITER ;;
CREATE TRIGGER `tri_locate_flag_insert` AFTER INSERT ON `locate` FOR EACH ROW BEGIN  
  -- 检查当前 环境，避免递归.  
  IF @disable_trigger IS NULL THEN  
    -- 设置禁用触发器标志.  
    SET @disable_trigger = 1;  
    -- 插入目标表  
        UPDATE `domain_index` SET `locate_flag` = new.flag WHERE `ID` = new.ID; 
    -- 恢复禁用触发器标志.  
    SET @disable_trigger = NULL;  
  END IF;  
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `tri_locate_flag_update`;
DELIMITER ;;
CREATE TRIGGER `tri_locate_flag_update` AFTER UPDATE ON `locate` FOR EACH ROW BEGIN  
  -- 检查当前 环境，避免递归.  
  IF @disable_trigger IS NULL THEN  
    -- 设置禁用触发器标志.  
    SET @disable_trigger = 1;  
    -- 插入目标表  
        UPDATE `domain_index` SET `locate_flag` = new.flag WHERE `ID` = new.ID; 
    -- 恢复禁用触发器标志.  
    SET @disable_trigger = NULL;  
  END IF;  
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `tri_malicious_flag_insert`;
DELIMITER ;;
CREATE TRIGGER `tri_malicious_flag_insert` AFTER INSERT ON `malicious_info` FOR EACH ROW BEGIN  
  -- 检查当前 环境，避免递归.  
  IF @disable_trigger IS NULL THEN  
    -- 设置禁用触发器标志.  
    SET @disable_trigger = 1;  
    -- 插入目标表  
        UPDATE `domain_index` SET `malicious_info_flag` = new.flag WHERE `ID` = new.ID; 
    -- 恢复禁用触发器标志.  
    SET @disable_trigger = NULL;  
  END IF;  
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `tri_malicious_flag_update`;
DELIMITER ;;
CREATE TRIGGER `tri_malicious_flag_update` AFTER UPDATE ON `malicious_info` FOR EACH ROW BEGIN  
  -- 检查当前 环境，避免递归.  
  IF @disable_trigger IS NULL THEN  
    -- 设置禁用触发器标志.  
    SET @disable_trigger = 1;  
    -- 插入目标表  
        UPDATE `domain_index` SET `malicious_info_flag` = new.flag WHERE `ID` = new.ID; 
        
    -- 恢复禁用触发器标志.  
    SET @disable_trigger = NULL;  
  END IF;  
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `tri_info_flag_insert`;
DELIMITER ;;
CREATE TRIGGER `tri_info_flag_insert` AFTER INSERT ON `other_info` FOR EACH ROW BEGIN  
  -- 检查当前 环境，避免递归.  
  IF @disable_trigger IS NULL THEN  
    -- 设置禁用触发器标志.  
    SET @disable_trigger = 1;  
    -- 插入目标表  
        UPDATE `domain_index` SET `other_info_flag` = new.flag WHERE `ID` = new.ID; 
    -- 恢复禁用触发器标志.  
    SET @disable_trigger = NULL;  
  END IF;  
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `tri_info_flag_update`;
DELIMITER ;;
CREATE TRIGGER `tri_info_flag_update` AFTER UPDATE ON `other_info` FOR EACH ROW BEGIN  
  -- 检查当前 环境，避免递归.  
  IF @disable_trigger IS NULL THEN  
    -- 设置禁用触发器标志.  
    SET @disable_trigger = 1;  
    -- 插入目标表  
        UPDATE `domain_index` SET `other_info_flag` = new.flag WHERE `ID` = new.ID; 
    -- 恢复禁用触发器标志.  
    SET @disable_trigger = NULL;  
  END IF;  
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `tri_whois_flag_insert`;
DELIMITER ;;
CREATE TRIGGER `tri_whois_flag_insert` AFTER INSERT ON `whois` FOR EACH ROW BEGIN  
  -- 检查当前 环境，避免递归.  
  IF @disable_trigger IS NULL THEN  
    -- 设置禁用触发器标志.  
    SET @disable_trigger = 1;  
    -- 插入目标表  
        UPDATE `domain_index` SET `whois_flag` = new.flag WHERE `ID` = new.ID; 
    -- 恢复禁用触发器标志.  
    SET @disable_trigger = NULL;  
  END IF;  
END
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `tri_whois_flag_update`;
DELIMITER ;;
CREATE TRIGGER `tri_whois_flag_update` AFTER UPDATE ON `whois` FOR EACH ROW BEGIN  
  -- 检查当前 环境，避免递归.  
  IF @disable_trigger IS NULL THEN  
    -- 设置禁用触发器标志.  
    SET @disable_trigger = 1;  
    -- 插入目标表  
        UPDATE `domain_index` SET `whois_flag` = new.flag WHERE `ID` = new.ID; 
    -- 恢复禁用触发器标志.  
    SET @disable_trigger = NULL;  
  END IF;  
END
;;
DELIMITER ;
