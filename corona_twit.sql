-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 15, 2020 at 10:03 AM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `phoenix`
--

-- --------------------------------------------------------

--
-- Table structure for table `corona_twit`
--

CREATE TABLE `corona_twit` (
  `Time` varchar(20) NOT NULL,
  `Description` longtext,
  `Usertweets` int(11) NOT NULL,
  `Source` varchar(25) NOT NULL,
  `Target` varchar(25) DEFAULT NULL,
  `Verified` varchar(6) NOT NULL,
  `Text` mediumtext NOT NULL,
  `Hashtag` longtext,
  `location` varchar(50) DEFAULT NULL,
  `Following` int(11) NOT NULL,
  `Followers` int(11) NOT NULL,
  `Retweets` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `corona_twit`
--
ALTER TABLE `corona_twit`
  ADD PRIMARY KEY (`Time`,`Usertweets`,`Source`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
