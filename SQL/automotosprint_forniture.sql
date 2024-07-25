CREATE DATABASE  IF NOT EXISTS `automotosprint` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `automotosprint`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: automotosprint
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `forniture`
--

DROP TABLE IF EXISTS `forniture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forniture` (
  `idforniture` int NOT NULL AUTO_INCREMENT,
  `codordine` int DEFAULT NULL,
  `codiceprod` int DEFAULT NULL,
  `ricambi` int DEFAULT NULL,
  `qt` int DEFAULT NULL,
  PRIMARY KEY (`idforniture`),
  KEY `codordine` (`codordine`),
  KEY `codiceprod` (`codiceprod`),
  CONSTRAINT `forniture_ibfk_1` FOREIGN KEY (`codordine`) REFERENCES `ordine` (`codordine`),
  CONSTRAINT `forniture_ibfk_2` FOREIGN KEY (`codiceprod`) REFERENCES `prodotto` (`codiceprod`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forniture`
--

LOCK TABLES `forniture` WRITE;
/*!40000 ALTER TABLE `forniture` DISABLE KEYS */;
INSERT INTO `forniture` VALUES (1,1,1,5,50),(2,2,2,10,80),(3,3,3,30,90),(4,4,4,20,80),(5,5,6,35,20),(6,6,6,3,5),(7,7,7,5,90),(8,10,8,2,4),(9,11,9,1,2),(10,12,10,2,20),(11,1,2,3,60),(13,3,5,40,100),(14,2,11,NULL,20),(15,4,9,NULL,60),(20,5,12,NULL,100);
/*!40000 ALTER TABLE `forniture` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-17 16:53:06
