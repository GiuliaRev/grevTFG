-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema new_tfg
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `new_tfg` ;

-- -----------------------------------------------------
-- Schema new_tfg
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `new_tfg` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
SHOW WARNINGS;
USE `new_tfg` ;

-- -----------------------------------------------------
-- Table `new_tfg`.`competences`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `new_tfg`.`competences` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `new_tfg`.`competences` (
  `id_kc` INT NOT NULL,
  `description` VARCHAR(1000) NOT NULL,
  `short_kc` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_kc`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `new_tfg`.`projects_general`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `new_tfg`.`projects_general` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `new_tfg`.`projects_general` (
  `id_proj` INT NOT NULL,
  `name` VARCHAR(200) NOT NULL,
  `link` VARCHAR(200) NOT NULL,
  `scope` VARCHAR(1000) NOT NULL,
  `cs_web_name` VARCHAR(200) NOT NULL,
  `cs_web_link` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id_proj`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE,
  UNIQUE INDEX `link_UNIQUE` (`link` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `new_tfg`.`projects_descriptions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `new_tfg`.`projects_descriptions` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `new_tfg`.`projects_descriptions` (
  `id_proj` INT NOT NULL,
  `description` MEDIUMTEXT NULL,
  INDEX `fk_projects_descriptions_projects_general1_idx` (`id_proj` ASC) VISIBLE,
  PRIMARY KEY (`id_proj`),
  CONSTRAINT `fk_projects_descriptions_projects_general1`
    FOREIGN KEY (`id_proj`)
    REFERENCES `new_tfg`.`projects_general` (`id_proj`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

ALTER TABLE `new_tfg`.`projects_descriptions`
MODIFY COLUMN `description` MEDIUMTEXT NOT NULL;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `new_tfg`.`projects_full_descriptions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `new_tfg`.`projects_full_descriptions` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `new_tfg`.`projects_full_descriptions` (
  `id_proj` INT NOT NULL,
  `full_desc` MEDIUMTEXT NOT NULL,
  PRIMARY KEY (`id_proj`),
  INDEX `fk_projects_full_descriptions_projects_general1_idx` (`id_proj` ASC) VISIBLE,
  CONSTRAINT `fk_projects_full_descriptions_projects_general1`
    FOREIGN KEY (`id_proj`)
    REFERENCES `new_tfg`.`projects_general` (`id_proj`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `new_tfg`.`projects_goals`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `new_tfg`.`projects_goals` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `new_tfg`.`projects_goals` (
  `id_proj` INT NOT NULL,
  `goal` VARCHAR(5000) NOT NULL,
  PRIMARY KEY (`id_proj`),
  INDEX `fk_projects_goals_projects_general1_idx` (`id_proj` ASC) VISIBLE,
  CONSTRAINT `fk_projects_goals_projects_general1`
    FOREIGN KEY (`id_proj`)
    REFERENCES `new_tfg`.`projects_general` (`id_proj`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `new_tfg`.`security_questions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `new_tfg`.`security_questions` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `new_tfg`.`security_questions` (
  `id_sq` INT NOT NULL,
  `question` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id_sq`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `new_tfg`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `new_tfg`.`users` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `new_tfg`.`users` (
  `username` VARCHAR(25) NOT NULL,
  `password` CHAR(64) NOT NULL,
  `id_sq` INT NULL DEFAULT NULL,
  `sec_ans` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`username`),
  INDEX `fk_users_security_questions1_idx` (`id_sq` ASC) VISIBLE,
  CONSTRAINT `fk_users_security_questions1`
    FOREIGN KEY (`id_sq`)
    REFERENCES `new_tfg`.`security_questions` (`id_sq`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `new_tfg`.`ratings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `new_tfg`.`ratings` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `new_tfg`.`ratings` (
  `username` VARCHAR(25) NOT NULL,
  `id_proj` INT NOT NULL,
  `rating` INT NOT NULL,
  PRIMARY KEY (`username`, `id_proj`),
  INDEX `fk_ratings_users1_idx` (`username` ASC) VISIBLE,
  INDEX `fk_ratings_projects1_idx` (`id_proj` ASC) VISIBLE,
  CONSTRAINT `fk_ratings_projects1`
    FOREIGN KEY (`id_proj`)
    REFERENCES `new_tfg`.`projects_general` (`id_proj`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_ratings_users1`
    FOREIGN KEY (`username`)
    REFERENCES `new_tfg`.`users` (`username`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `new_tfg`.`users_have_competences`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `new_tfg`.`users_have_competences` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `new_tfg`.`users_have_competences` (
  `username` VARCHAR(25) NOT NULL,
  `id_kc` INT NOT NULL,
  PRIMARY KEY (`username`, `id_kc`),
  INDEX `fk_users_has_competences_competences1_idx` (`id_kc` ASC) VISIBLE,
  INDEX `fk_users_has_competences_users_idx` (`username` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_competences_competences1`
    FOREIGN KEY (`id_kc`)
    REFERENCES `new_tfg`.`competences` (`id_kc`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_users_has_competences_users`
    FOREIGN KEY (`username`)
    REFERENCES `new_tfg`.`users` (`username`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `new_tfg`.`users_have_keywords`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `new_tfg`.`users_have_keywords` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `new_tfg`.`users_have_keywords` (
  `username` VARCHAR(25) NOT NULL,
  `keyword` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`username`, `keyword`),
  INDEX `fk_user_has_keywords_users1_idx` (`username` ASC) VISIBLE,
  CONSTRAINT `fk_user_has_keywords_users1`
    FOREIGN KEY (`username`)
    REFERENCES `new_tfg`.`users` (`username`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
