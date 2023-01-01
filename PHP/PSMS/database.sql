-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 10, 2020 at 12:41 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `psms`
--

-- --------------------------------------------------------

--
-- Table structure for table `allowance`
--

CREATE TABLE `allowance` (
  `id` int(11) NOT NULL,
  `eid` int(11) NOT NULL,
  `smonth` varchar(20) NOT NULL,
  `fyear` int(11) NOT NULL,
  `actual` int(11) NOT NULL,
  `agp` int(11) NOT NULL,
  `da` int(11) NOT NULL,
  `hra` int(11) NOT NULL,
  `med` int(11) NOT NULL,
  `other1` int(11) NOT NULL,
  `gtotal` int(11) NOT NULL,
  `wf` int(11) NOT NULL,
  `net1` int(11) NOT NULL,
  `released` int(11) NOT NULL,
  `pf` int(11) NOT NULL,
  `pfadv` int(11) NOT NULL,
  `lic` int(11) NOT NULL,
  `it` int(11) NOT NULL,
  `qrent` int(11) NOT NULL,
  `rev_adv` int(11) NOT NULL,
  `dtotal` int(11) NOT NULL,
  `net2` int(11) NOT NULL,
  `wa` int(11) NOT NULL,
  `fadv` int(11) NOT NULL,
  `ht` int(11) NOT NULL,
  `marriage_med` int(11) NOT NULL,
  `sal_adv` int(11) NOT NULL,
  `rev_asso` int(11) NOT NULL,
  `other2` int(11) NOT NULL,
  `other3` int(11) NOT NULL,
  `remarks1` varchar(110) NOT NULL,
  `remarks2` varchar(110) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `clg_details`
--

CREATE TABLE `clg_details` (
  `id` int(11) NOT NULL,
  `clg_name` varchar(255) NOT NULL,
  `clg_add` varchar(255) NOT NULL,
  `principal` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `principal_photo` varchar(255) NOT NULL,
  `logo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `id` int(11) NOT NULL,
  `emp_name` varchar(200) NOT NULL,
  `mname` varchar(200) NOT NULL,
  `fname` varchar(200) NOT NULL,
  `sname` varchar(200) NOT NULL,
  `dob` varchar(12) NOT NULL,
  `emp_add` varchar(200) NOT NULL,
  `category` varchar(50) NOT NULL,
  `designation` varchar(100) NOT NULL,
  `marital_sts` varchar(50) NOT NULL,
  `mob1` varchar(13) NOT NULL,
  `mob2` varchar(13) NOT NULL,
  `email` varchar(100) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `grade` varchar(50) NOT NULL,
  `department` varchar(50) NOT NULL,
  `doa` varchar(13) NOT NULL,
  `salary` int(11) NOT NULL,
  `emp_photo` varchar(100) NOT NULL,
  `doc1` varchar(100) NOT NULL,
  `doc2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `allowance`
--
ALTER TABLE `allowance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clg_details`
--
ALTER TABLE `clg_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `allowance`
--
ALTER TABLE `allowance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `clg_details`
--
ALTER TABLE `clg_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
