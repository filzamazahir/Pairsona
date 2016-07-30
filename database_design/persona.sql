-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema personas_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema personas_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `personas_db` DEFAULT CHARACTER SET utf8 ;
USE `personas_db` ;

-- -----------------------------------------------------
-- Table `personas_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `personas_db`.`users` (
  `id` INT NOT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `helper` TINYINT(1) NULL,
  `zipcode` VARCHAR(45) NULL,
  `description` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `personas_db`.`helper`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `personas_db`.`helper` (
  `user_id` INT NOT NULL,
  `realestate` TINYINT(1) NULL,
  `finances` TINYINT(1) NULL,
  `medicalcare` TINYINT(1) NULL,
  `automobile` TINYINT(1) NULL,
  `lang_tutor` TINYINT(1) NULL,
  `lang_translator` TINYINT(1) NULL,
  `babysitter` TINYINT(1) NULL,
  `social` TINYINT(1) NULL,
  `previous_newcomer` TINYINT(1) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  INDEX `fk_helper_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_helper_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `personas_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `personas_db`.`newcomer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `personas_db`.`newcomer` (
  `user_id` INT NOT NULL,
  `date_entry` DATETIME NULL,
  `country_origin` VARCHAR(45) NULL,
  `created_at` TEXT NULL,
  `updated_at` TEXT NULL,
  CONSTRAINT `fk_refugee_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `personas_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
