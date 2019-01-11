create database aip_show charset=utf8;
USE aip_show;


SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


--
-- 数据库: `aip_show`
--

-- --------------------------------------------------------

--
-- 表的结构 `show_pic_detect`
--

CREATE TABLE IF NOT EXISTS `show_pic_detect` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '自增',
  `picture_id` int(10) NOT NULL COMMENT 'picture id',
  `age` int(10) NOT NULL COMMENT '年龄',
  `beauty` float NOT NULL COMMENT '美丑打分，范围0-100，越大表示越美',
  `expression` varchar(64) NOT NULL COMMENT '表情',
  `face_shape` varchar(64) NOT NULL COMMENT '脸型',
  `gender` tinyint(4) NOT NULL COMMENT '1:男性 2:女性 0:不可知',
  `glasses` varchar(64) NOT NULL COMMENT '是否带眼镜',
  `quality` varchar(256) NOT NULL COMMENT '人脸质量信息',
  `other` varchar(4096) NOT NULL COMMENT '整体结果保存',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `last_modified_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  KEY `picture_id` (`picture_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='人脸检测';

-- --------------------------------------------------------

--
-- 表的结构 `show_topic`
--

CREATE TABLE IF NOT EXISTS `show_topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增',
  `org_topic_id` varchar(32) NOT NULL COMMENT '源主题ID',
  `topic_from` varchar(16) NOT NULL COMMENT '主题来源， njtu, sjtu,fudan',
  `board` varchar(32) NOT NULL,
  `title` varchar(256) NOT NULL COMMENT '标题',
  `body` varchar(4096) NOT NULL COMMENT '内容',
  `pic_list` varchar(256) NOT NULL COMMENT '图片列表ID',
  `sex` tinyint(2) NOT NULL COMMENT '性别',
  `qq` varchar(32) NOT NULL COMMENT 'qq',
  `weixin` varchar(64) NOT NULL COMMENT '微信',
  `email` varchar(256) NOT NULL COMMENT '邮箱',
  `topic_url` varchar(128) NOT NULL COMMENT '源地址',
  `author_name` varchar(64) NOT NULL COMMENT '发帖人',
  `author_id` int(10) NOT NULL COMMENT '发帖人ID',
  `author_homepage` varchar(128) NOT NULL COMMENT '发帖人主页',
  `post_time` datetime NOT NULL COMMENT '帖子创建时间',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `last_modified_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  KEY `org_topic_id` (`org_topic_id`,`topic_from`,`board`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `show_topic_pic`
--

CREATE TABLE IF NOT EXISTS `show_topic_pic` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '自增',
  `topic_id` int(10) NOT NULL COMMENT '主题ID',
  `org_topic_id` varchar(32) NOT NULL COMMENT '源主题ID',
  `topic_from` varchar(16) NOT NULL COMMENT '主题来源， njtu, sjtu,fudan',
  `url` varchar(256) NOT NULL COMMENT '链接地址',
  `content` text NOT NULL COMMENT '图片内容',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '0:正常，1:抓取中, 2: 删除',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `last_modified_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  KEY `topic_id` (`topic_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `show_topic_stat`
--

CREATE TABLE IF NOT EXISTS `show_topic_stat` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'topic id',
  `topic_id` int(10) NOT NULL COMMENT 'org topic id',
  `org_topic_id` varchar(32) NOT NULL COMMENT '源主题ID',
  `topic_from` varchar(16) NOT NULL COMMENT '主题来源， njtu, sjtu,fudan',
  `reply_count` int(10) NOT NULL COMMENT '回帖数',
  `popular_count` int(10) NOT NULL COMMENT '人气数',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `last_modified_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  KEY `topic_id` (`topic_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;