/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50728
 Source Host           : localhost:3306
 Source Schema         : hawkeye2

 Target Server Type    : MySQL
 Target Server Version : 50728
 File Encoding         : 65001

 Date: 14/06/2024 10:33:17
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for scan
-- ----------------------------
DROP TABLE IF EXISTS `scan`;
CREATE TABLE `scan` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `path` varchar(100) DEFAULT NULL,
  `filename` varchar(50) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `status` tinyint(4) DEFAULT '-1',
  `taskid` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
