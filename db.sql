/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - job_mapper
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`job_mapper` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `job_mapper`;

/*Table structure for table `employee` */

DROP TABLE IF EXISTS `employee`;

CREATE TABLE `employee` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `cname` varchar(100) DEFAULT NULL,
  `roll` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `age` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `dist` varchar(100) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `employee` */

insert  into `employee`(`id`,`name`,`email`,`pwd`,`cname`,`roll`,`pno`,`addr`,`gender`,`age`,`state`,`dist`,`photo`) values (1,'nakku','nakku@gmail.com','1234','TCS','python developer','8574589654','TPT','Female','23','Madya Pradesh','Gwalior','static/profiles/Capture.PNG');

/*Table structure for table `job_applications` */

DROP TABLE IF EXISTS `job_applications`;

CREATE TABLE `job_applications` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  `disc` varchar(100) DEFAULT NULL,
  `salary` varchar(100) DEFAULT NULL,
  `exp` varchar(100) DEFAULT NULL,
  `skill` varchar(100) DEFAULT NULL,
  `cname` varchar(100) DEFAULT NULL,
  `loc` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `emp_email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `job_applications` */

/*Table structure for table `job_seeker` */

DROP TABLE IF EXISTS `job_seeker`;

CREATE TABLE `job_seeker` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `age` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `dist` varchar(100) DEFAULT NULL,
  `pgoto` varchar(100) DEFAULT NULL,
  `resume` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `job_seeker` */

/*insert  into `job_seeker`(`id`,`name`,`email`,`pwd`,`pno`,`gender`,`age`,`addr`,`state`,`dist`,`pgoto`,`resume`) values (1,'preeti','preeti@gmail.com','1234','9685745896','Female','23','TPT','Karnataka','Bangalore Urban','static/profiles/Screenshot 2024-02-23 101500.png',NULL);*/

/*Table structure for table `jobs_info` */

DROP TABLE IF EXISTS `jobs_info`;

CREATE TABLE `jobs_info` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL,
  `cname` varchar(100) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  `disc` varchar(100) DEFAULT NULL,
  `salary` varchar(100) DEFAULT NULL,
  `exp` varchar(100) DEFAULT NULL,
  `skill` varchar(100) DEFAULT NULL,
  `qual` varchar(100) DEFAULT NULL,
  `notf` varchar(100) DEFAULT NULL,
  `loc` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `cemail` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `jobs_info` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
