/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 100427
 Source Host           : localhost:3306
 Source Schema         : chatroom

 Target Server Type    : MySQL
 Target Server Version : 100427
 File Encoding         : 65001

 Date: 13/04/2023 10:50:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for messages
-- ----------------------------
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `message` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `receiver_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of messages
-- ----------------------------
INSERT INTO `messages` VALUES (1, 'SGVsbG8sIE1pY2hlYWw=', '2023-04-13 00:08:09', 'John', 'Micheal');
INSERT INTO `messages` VALUES (2, 'TXkgbmFtZSBpcyBKb2huIFNtaXRo', '2023-04-13 00:08:25', 'John', 'Micheal');
INSERT INTO `messages` VALUES (3, 'SGVsbG8hIEpvaG4=', '2023-04-13 10:16:40', 'Siddu Reddy', 'John');
INSERT INTO `messages` VALUES (4, '8J+YjkhpISBTaWRkdS4=', '2023-04-13 10:17:09', 'John', NULL);
INSERT INTO `messages` VALUES (5, 'SG93IGFyZSB5b3U/', '2023-04-13 10:17:18', 'John', NULL);
INSERT INTO `messages` VALUES (6, '8J+Yh0hpLCBTaWRkdQ==', '2023-04-13 10:17:46', 'John', 'Siddu Reddy');
INSERT INTO `messages` VALUES (7, 'SG93IGFyZSB5b3U/', '2023-04-13 10:17:53', 'John', 'Siddu Reddy');
INSERT INTO `messages` VALUES (14, '8J+YjSBIZWxsbywgU2lkZHUh', '2023-04-13 10:40:42', 'Futuresea', 'Siddu Reddy');
INSERT INTO `messages` VALUES (15, 'SG93IGFyZSB5b3U/', '2023-04-13 10:40:47', 'Futuresea', 'Siddu Reddy');
INSERT INTO `messages` VALUES (16, 'SGVsbG8=', '2023-04-13 10:41:12', 'Siddu Reddy', 'Futuresea');
INSERT INTO `messages` VALUES (17, 'SSdtIGZpbmUsIGFuZCB5b3U/', '2023-04-13 10:41:25', 'Siddu Reddy', 'Futuresea');
INSERT INTO `messages` VALUES (18, 'TWUsIHRvby4=', '2023-04-13 10:41:34', 'Futuresea', 'Siddu Reddy');
INSERT INTO `messages` VALUES (19, 'SGksIEpvaG4=', '2023-04-13 10:41:47', 'Futuresea', 'John');
INSERT INTO `messages` VALUES (20, 'V2hhdCBhcmUgeW91IGRvaW5nIG5vdz8=', '2023-04-13 10:41:56', 'Futuresea', 'John');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `avatar_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (3, 'a@gmail.com', '4297f44b13955235245b2497399d7a93', 'Micheal', 'http://localhost:5000/static/images/002.jpg');
INSERT INTO `users` VALUES (4, 'z@gmail.com', '4297f44b13955235245b2497399d7a93', 'John', 'http://localhost:5000/static/images/005.jpg');
INSERT INTO `users` VALUES (5, 'svvrcloud18@gmail.com', '4297f44b13955235245b2497399d7a93', 'Siddu Reddy', 'http://localhost:5000/static/images/003.jpg');
INSERT INTO `users` VALUES (7, 'futuresea.talent.dev713@gmail.com', '4297f44b13955235245b2497399d7a93', 'Futuresea', 'http://localhost:5000/static/images/004.jpg');

SET FOREIGN_KEY_CHECKS = 1;
