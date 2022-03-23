/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : localhost:3306
 Source Schema         : spider

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 23/03/2022 20:52:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for zongheng
-- ----------------------------
DROP TABLE IF EXISTS `zongheng`;
CREATE TABLE `zongheng`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '序号',
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `img_src` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `author` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `introduce` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `latest_chapter` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `bookUrl`(`url`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99494 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
