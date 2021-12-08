-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: classmysql.engr.oregonstate.edu:3306
-- Generation Time: Mar 17, 2020 at 08:26 PM
-- Server version: 10.4.11-MariaDB-log
-- PHP Version: 7.0.33

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_chaissoj`
--

-- --------------------------------------------------------

--
-- Table structure for table `gr6_carts`
--

DROP TABLE IF EXISTS `gr6_carts`;
CREATE TABLE `gr6_carts` (
  `cart_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gr6_carts`
--

INSERT INTO `gr6_carts` (`cart_id`, `customer_id`) VALUES
(3, NULL),
(17, NULL),
(18, NULL),
(1, 1),
(2, 1),
(4, 1),
(24, 1),
(5, 2),
(19, 2),
(20, 2),
(21, 2),
(6, 3),
(7, 4),
(8, 5),
(9, 6),
(10, 7),
(23, 7),
(11, 8),
(12, 11),
(13, 12),
(14, 14),
(22, 14),
(15, 18),
(25, 18),
(16, 19);

-- --------------------------------------------------------

--
-- Table structure for table `gr6_customers`
--

DROP TABLE IF EXISTS `gr6_customers`;
CREATE TABLE `gr6_customers` (
  `customer_id` int(11) NOT NULL,
  `fname` varchar(225) NOT NULL,
  `lname` varchar(225) NOT NULL,
  `email` varchar(225) NOT NULL,
  `handle` varchar(225) DEFAULT NULL,
  `credit_card` varchar(225) DEFAULT NULL,
  `zip_code` varchar(225) NOT NULL,
  `state` varchar(225) NOT NULL,
  `city` varchar(225) NOT NULL,
  `street` varchar(225) NOT NULL,
  `street_number` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gr6_customers`
--

INSERT INTO `gr6_customers` (`customer_id`, `fname`, `lname`, `email`, `handle`, `credit_card`, `zip_code`, `state`, `city`, `street`, `street_number`) VALUES
(1, 'Jamie', 'Chaisson', 'Zomberder@mail.com', 'Zomberder', '888888', '99999', 'Moon', 'Somewhere', 'Nowhere', '123'),
(2, 'Casey', 'Levy', 'm@n.com', 'Orc Arms', NULL, '99999', 'FL', 'Nowhere', 'Somewhere Ln', '456'),
(3, 'T Rex', 'Dino', 'jurassic@meteor.com', 'Lizard', 'dfasdff', 'dsfasdf', 'dsfasd', 'asdf', 'dsfa', 'fdads'),
(4, 'Sylver', 'Chaisson', 'awesome@mail.com', 'Awesome', 'dsfasdf', 'dfasdff', 'dsfasd', 'asdf', 'dsfa', 'fdads'),
(5, 'Jim', 'Morrison', 'JM@g.com', 'The Kizard King', '123456789999', '77777', 'Arizona', 'Sedona', 'Love Street', '123'),
(6, 'Katie', 'Morrison', 'JM@g.com', 'The Kizard Queen', '123456789999', '77777', 'Arizona', 'Sedona', 'Love Street', '123'),
(7, 'Biff', 'Bifferson', 'JM@g.com', 'Blue', '77778', '123456789999', 'Arizona', 'Pheonix', 'Article', '123'),
(8, 'Mr.', 'Robot', 'MrT@ATeam.com', 'Tureaud', '999999999999', '3245', 'Illinois', 'Chicago', 'Pity The Fool Lane', '345'),
(11, 'Cthulu', 'Spiffy', 'CS@mail.com', 'BadGuy', '666-666-666-666', '66666', 'Ur', 'Babylon', 'Tartarus', '666'),
(12, 'Thanos', 'The Destroyer', 'prettyInPink@mail.com', 'Biff', '234534613452724', '24515', 'Order', 'Glory Town', 'Red st', '13242'),
(14, 'jackson', 'polloc', 'fsga@lasduuoo.klhguy', 'Drunk', 'dsfasdf', 'dfasdff', 'dsfasd', 'asdf', 'dsfa', 'fdads'),
(18, 'Jason', 'Borne', 'JB@mail.com', 'hiccup', '235234', '123456789999', 'dood', 'doood', 'goode', '2532'),
(19, 'jaeger', 'The', 'KLR@mail.com', 'Furball', '11111', '123456789999', 'Oreagon', 'Kitty', 'scratchingpost', '567'),
(27, 'Arrow', 'Mcfairlane', 'AM@g.com', 'Arr', '', '99999', 'New York', 'New York', 'Red St', '123');

-- --------------------------------------------------------

--
-- Table structure for table `gr6_games`
--

DROP TABLE IF EXISTS `gr6_games`;
CREATE TABLE `gr6_games` (
  `game_id` int(11) NOT NULL,
  `game_title` varchar(225) NOT NULL,
  `sell_price` decimal(6,2) NOT NULL,
  `discount` decimal(2,2) DEFAULT 0.00,
  `critic_rating` tinyint(1) DEFAULT NULL,
  `info` varchar(225) DEFAULT 'No Info Available'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gr6_games`
--

INSERT INTO `gr6_games` (`game_id`, `game_title`, `sell_price`, `discount`, `critic_rating`, `info`) VALUES
(1, 'Zelda', '20.00', '0.00', 5, 'Save the princess and collect the triforce'),
(2, 'Action Jackson', '15.00', '0.05', 3, 'Dont stop until you beat the bad guy!'),
(3, 'Four Swords', '3.00', '0.00', 2, 'a'),
(4, 'Bomberman', '5.00', '0.50', 1, 'The bombs be dropping. Get out of the way before you go Ka-Bloom!'),
(14, 'E-Zero', '20.00', '0.10', 1, 'A cheap knock off of F-Zero'),
(15, 'Pac Man', '5.55', '0.00', 4, 'Inky, Blinky, Pinky, and Clyde! Oh My!'),
(17, 'Call Of Duty', '50.00', '0.00', 1, 'Same game every year.'),
(18, 'Stardew Valley', '60.00', '0.00', 5, 'The best farming game');

-- --------------------------------------------------------

--
-- Table structure for table `gr6_games_carts`
--

DROP TABLE IF EXISTS `gr6_games_carts`;
CREATE TABLE `gr6_games_carts` (
  `cart_id` int(11) NOT NULL,
  `game_id` int(11) NOT NULL,
  `item_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gr6_games_carts`
--

INSERT INTO `gr6_games_carts` (`cart_id`, `game_id`, `item_number`) VALUES
(1, 2, 1),
(2, 1, 3),
(2, 4, 1),
(3, 1, 7),
(3, 2, 1),
(3, 3, 4),
(3, 4, 2),
(3, 14, 3),
(3, 15, 6),
(4, 15, 2),
(5, 2, 1),
(6, 1, 2),
(6, 4, 1),
(7, 2, 1),
(7, 14, 2),
(8, 15, 2),
(9, 4, 1),
(10, 1, 2),
(10, 3, 1),
(11, 3, 1),
(12, 2, 2),
(12, 3, 1),
(13, 3, 1),
(13, 4, 2),
(14, 14, 1),
(14, 15, 2),
(15, 2, 3),
(15, 4, 1),
(16, 4, 1),
(16, 14, 2),
(17, 1, 2),
(17, 4, 1),
(18, 1, 1),
(19, 1, 1),
(20, 1, 2),
(20, 15, 1),
(22, 2, 0),
(23, 14, 0),
(25, 17, 1);

-- --------------------------------------------------------

--
-- Table structure for table `gr6_library`
--

DROP TABLE IF EXISTS `gr6_library`;
CREATE TABLE `gr6_library` (
  `library_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `game_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gr6_library`
--

INSERT INTO `gr6_library` (`library_id`, `customer_id`, `game_id`) VALUES
(3, 1, 1),
(4, 1, 4),
(5, 1, NULL),
(6, NULL, 1),
(7, NULL, 2),
(8, NULL, 3),
(9, NULL, 4),
(10, NULL, NULL),
(11, NULL, 14),
(12, NULL, 15),
(13, 1, NULL),
(14, 1, 15),
(15, 2, 2),
(16, 2, NULL),
(17, 3, 1),
(18, 3, 4),
(19, 4, 2),
(20, 4, 14),
(21, 5, NULL),
(22, 5, 15),
(23, 6, 4),
(24, 6, NULL),
(25, 7, 1),
(26, 7, 3),
(27, 8, 3),
(28, 8, NULL),
(29, 11, 2),
(30, 11, 3),
(31, 12, 3),
(33, 14, 14),
(35, 18, 2),
(36, 18, 4),
(37, 18, NULL),
(38, 19, 4),
(39, 19, 14),
(40, NULL, 1),
(41, NULL, 4),
(43, 2, 1),
(44, 2, 15);

-- --------------------------------------------------------

--
-- Table structure for table `gr6_orders`
--

DROP TABLE IF EXISTS `gr6_orders`;
CREATE TABLE `gr6_orders` (
  `order_number` int(11) NOT NULL,
  `cart_id` int(11) NOT NULL,
  `tax` decimal(6,2) NOT NULL,
  `total` decimal(6,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gr6_orders`
--

INSERT INTO `gr6_orders` (`order_number`, `cart_id`, `tax`, `total`) VALUES
(1, 1, '1.00', '13.00'),
(2, 2, '8.00', '88.00'),
(3, 3, '6.00', '72.54'),
(4, 4, '1.00', '7.54'),
(5, 5, '1.00', '13.99'),
(6, 6, '2.00', '27.00'),
(7, 7, '3.00', '35.00'),
(8, 8, '1.00', '7.54'),
(9, 9, '1.00', '6.99'),
(10, 10, '2.00', '25.00'),
(11, 11, '0.00', '3.99'),
(12, 12, '1.00', '16.00'),
(13, 13, '1.00', '9.00'),
(14, 14, '2.00', '27.55'),
(15, 15, '2.00', '19.99'),
(16, 16, '2.00', '27.00'),
(17, 17, '2.00', '27.00'),
(18, 18, '2.00', '22.00'),
(19, 20, '2.00', '27.55'),
(20, 25, '9.97', '105.00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `gr6_carts`
--
ALTER TABLE `gr6_carts`
  ADD PRIMARY KEY (`cart_id`),
  ADD KEY `gr6_cart_fk1` (`customer_id`);

--
-- Indexes for table `gr6_customers`
--
ALTER TABLE `gr6_customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `handle` (`handle`);

--
-- Indexes for table `gr6_games`
--
ALTER TABLE `gr6_games`
  ADD PRIMARY KEY (`game_id`),
  ADD UNIQUE KEY `game_title` (`game_title`);

--
-- Indexes for table `gr6_games_carts`
--
ALTER TABLE `gr6_games_carts`
  ADD PRIMARY KEY (`cart_id`,`game_id`),
  ADD KEY `gr6_games_carts_fk2` (`game_id`);

--
-- Indexes for table `gr6_library`
--
ALTER TABLE `gr6_library`
  ADD PRIMARY KEY (`library_id`),
  ADD KEY `gr6_library_fk2` (`game_id`),
  ADD KEY `gr6_library_fk1` (`customer_id`);

--
-- Indexes for table `gr6_orders`
--
ALTER TABLE `gr6_orders`
  ADD PRIMARY KEY (`order_number`),
  ADD KEY `gr6_orders_fk1` (`cart_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `gr6_carts`
--
ALTER TABLE `gr6_carts`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `gr6_customers`
--
ALTER TABLE `gr6_customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `gr6_games`
--
ALTER TABLE `gr6_games`
  MODIFY `game_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `gr6_library`
--
ALTER TABLE `gr6_library`
  MODIFY `library_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `gr6_orders`
--
ALTER TABLE `gr6_orders`
  MODIFY `order_number` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `gr6_carts`
--
ALTER TABLE `gr6_carts`
  ADD CONSTRAINT `gr6_cart_fk1` FOREIGN KEY (`customer_id`) REFERENCES `gr6_customers` (`customer_id`) ON DELETE SET NULL;

--
-- Constraints for table `gr6_games_carts`
--
ALTER TABLE `gr6_games_carts`
  ADD CONSTRAINT `gr6_games_carts_fk1` FOREIGN KEY (`cart_id`) REFERENCES `gr6_carts` (`cart_id`),
  ADD CONSTRAINT `gr6_games_carts_fk2` FOREIGN KEY (`game_id`) REFERENCES `gr6_games` (`game_id`) ON DELETE CASCADE;

--
-- Constraints for table `gr6_library`
--
ALTER TABLE `gr6_library`
  ADD CONSTRAINT `gr6_library_fk1` FOREIGN KEY (`customer_id`) REFERENCES `gr6_customers` (`customer_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `gr6_library_fk2` FOREIGN KEY (`game_id`) REFERENCES `gr6_games` (`game_id`) ON DELETE SET NULL;

--
-- Constraints for table `gr6_orders`
--
ALTER TABLE `gr6_orders`
  ADD CONSTRAINT `gr6_orders_fk1` FOREIGN KEY (`cart_id`) REFERENCES `gr6_carts` (`cart_id`);
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
