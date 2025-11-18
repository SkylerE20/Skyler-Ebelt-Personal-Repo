-- Tables

CREATE TYPE sex_type AS ENUM ('Male', 'Female', 'Unknown');
CREATE TABLE Dog (
    dog_id INT GENERATED ALWAYS AS IDENTITY,
    dog_name VARCHAR(250) NOT NULL,
    sex sex_type NOT NULL,
    altered BOOLEAN NOT NULL,
    age INTEGER NOT NULL,
    description VARCHAR(500),
    surrender_date DATE NOT NULL,
    surrenderer_phone_number VARCHAR(20),
    surrendered_by_animal_control BOOLEAN NOT NULL,
    volunteer_email VARCHAR(250) NOT NULL,
    PRIMARY KEY (dog_id)
);

CREATE TABLE IsBreed (
    dog_id INT NOT NULL,
    breed_name VARCHAR(250) NOT NULL,
    PRIMARY KEY (dog_id, breed_name)
);

CREATE TABLE Breed (
    breed_name VARCHAR(250) NOT NULL,
    PRIMARY KEY (breed_name)
);

CREATE TABLE Microchip (
    microchip_id INT NOT NULL,
    dog_id INT NOT NULL,
    vendor_name VARCHAR(250) NOT NULL,
    PRIMARY KEY (microchip_id)
);

CREATE TABLE MicrochipVendor (
    vendor_name VARCHAR(250) NOT NULL,
    PRIMARY KEY (vendor_name)
);

CREATE TABLE Volunteer (
    email_address VARCHAR(250) NOT NULL,
    volunteer_password VARCHAR(250) NOT NULL,
    first_name VARCHAR(250) NOT NULL,
    last_name VARCHAR(250) NOT NULL,
    birth_date DATE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    PRIMARY KEY (email_address)
);

CREATE TABLE ExecutiveDirector (
    email_address VARCHAR(250) NOT NULL,
    PRIMARY KEY (email_address)
);

CREATE TABLE Adopter (
    applicant_email VARCHAR(250) NOT NUll,
    first_name VARCHAR(250) NOT NULL,
    last_name VARCHAR(250) NOT NULL,
    applicant_phone VARCHAR(20) NOT NULL,
    household_size INT NOT NULL,
    state_abbrev CHAR(2) NOT NULL,
    city VARCHAR(250) NOT NULL,
    street VARCHAR(250) NOT NULL,
    ZIP_code VARCHAR(250) NOT NULL,
    PRIMARY KEY (applicant_email)
);

CREATE TABLE Application (
    applicant_email VARCHAR(250) NOT NULL,
    application_date DATE NOT NULL,
    PRIMARY KEY (applicant_email, application_date)
);

CREATE TABLE ApprovedApplication (
    applicant_email VARCHAR(250) NOT NULL,
    application_date DATE NOT NULL,
    accept_date DATE NOT NULL,
    PRIMARY KEY (applicant_email, application_date)
);

CREATE TABLE RejectedApplication (
    applicant_email VARCHAR(250) NOT NULL,
    application_date DATE NOT NULL,
    reject_date DATE NOT NULL,
    PRIMARY KEY (applicant_email, application_date)
);

CREATE TABLE AdoptedRelation (
    applicant_email VARCHAR(250) NOT NULL,
    application_date DATE NOT NULL,
    dog_id INT NOT NULL,
    adoption_date DATE NOT NULL,
    fee DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (applicant_email, application_date, dog_id)
);

CREATE TABLE Expense (
    dog_id INT NOT NULL,
    expense_date DATE NOT NULL,
    expense_vendor VARCHAR(250) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    category_name VARCHAR(250) NOT NULL,
    PRIMARY KEY (dog_id, expense_date, expense_vendor)
);

CREATE TABLE Category (
    category_name VARCHAR(250) NOT NULL,
    PRIMARY KEY (category_name)
);

-- Constraints   Foreign Keys: FK_ChildTable_childColumn_ParentTable_parentColumn

ALTER TABLE Dog
    ADD CONSTRAINT FK_Dog_volunteerEmail_Volunteer_volunteerEmail FOREIGN KEY (volunteer_email) REFERENCES Volunteer (email_address);

ALTER TABLE IsBreed
    ADD CONSTRAINT FK_IsBreed_dogId_Dog_dogID FOREIGN KEY (dog_id) REFERENCES Dog (dog_id),
    ADD CONSTRAINT FK_IsBreed_breedName_Breed_breedName FOREIGN KEY (breed_name) REFERENCES Breed (breed_name);

ALTER TABLE Microchip
    ADD CONSTRAINT FK_Microchip_vendorName_MicrochipVendor_vendorName FOREIGN KEY (vendor_name) REFERENCES MicrochipVendor (vendor_name);

ALTER TABLE ExecutiveDirector
    ADD CONSTRAINT FK_ExecutiveDirector_emailAddress_Volunteer_emailAddress FOREIGN KEY (email_address) REFERENCES Volunteer (email_address);

ALTER TABLE Application
    ADD CONSTRAINT FK_Application_applicantEmail_Adopter_applicantEmail FOREIGN KEY (applicant_email) REFERENCES Adopter (applicant_email);

ALTER TABLE ApprovedApplication
    ADD CONSTRAINT FK_ApprovedApplication_EmailDate_Adopter_EmailDate FOREIGN KEY (applicant_email, application_date) REFERENCES Application (applicant_email, application_date);

ALTER TABLE RejectedApplication
    ADD CONSTRAINT FK_RejectedApplication_EmailDate_Adopter_EmailDate FOREIGN KEY (applicant_email, application_date) REFERENCES Application (applicant_email, application_date);

ALTER TABLE AdoptedRelation
    ADD CONSTRAINT FK_AdoptedRelation_EmailDate_Adopter_EmailDate FOREIGN KEY (applicant_email, application_date) REFERENCES Application (applicant_email, application_date),
    ADD CONSTRAINT FK_AdoptedRelation_dogID_Dog_dogID FOREIGN KEY (dog_id) REFERENCES Dog (dog_id);

ALTER TABLE Expense
    ADD CONSTRAINT FK_Expense_dogID_Dog_dogID FOREIGN KEY (dog_id) REFERENCES Dog (dog_id),
    ADD CONSTRAINT FK_Expense_categoryName_Category_categoryName FOREIGN KEY (category_name) REFERENCES Category (category_name);
