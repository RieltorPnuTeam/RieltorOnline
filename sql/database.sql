CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    IsStudent BOOLEAN NOT NULL,
    Name VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(20),
    UserType ENUM('орендар', 'власник') NOT NULL,
    RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Apartments (
    ApartmentID INT AUTO_INCREMENT PRIMARY KEY,
    OwnerID INT NOT NULL,
    Type ENUM('квартира', 'приватний будинок') NOT NULL,
    City VARCHAR(255) NOT NULL,
    Street VARCHAR(255) NOT NULL,
    HouseNum VARCHAR(20) NOT NULL,
    FlatNum VARCHAR(20),
    Price DECIMAL(10, 2) NOT NULL,
    RoomCount INT NOT NULL,
    Description TEXT,
    Comfort TEXT,
    Infrastructure TEXT,
    Renovation TEXT,
    Appliances TEXT,
    MaxResidents INT NOT NULL,
    CurrentResidents INT,
    IsRented ENUM('вільна', 'зайнята', 'відкрита для співмешканців') NOT NULL,
    CreationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FavoriteCount INT DEFAULT 0,
    FOREIGN KEY (OwnerID) REFERENCES Users(UserID) ON DELETE CASCADE
);

CREATE TABLE Favorites (
    FavoriteID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    ApartmentID INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (ApartmentID) REFERENCES Apartments(ApartmentID) ON DELETE CASCADE
);

CREATE TABLE ApartmentComments (
    CommentID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    ApartmentID INT NOT NULL,
    Content TEXT NOT NULL,
    Rating INT CHECK (Rating >= 1 AND Rating <= 5),
    DateAdded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (ApartmentID) REFERENCES Apartments(ApartmentID) ON DELETE CASCADE
);

CREATE TABLE UserComments (
    CommentID INT AUTO_INCREMENT PRIMARY KEY,
    AuthorID INT NOT NULL,
    TargetUserID INT NOT NULL,
    Content TEXT NOT NULL,
    Rating INT CHECK (Rating >= 1 AND Rating <= 5),
    DateAdded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AuthorID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (TargetUserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

CREATE TABLE Roommates (
    RoommateID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    ApartmentID INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (ApartmentID) REFERENCES Apartments(ApartmentID) ON DELETE CASCADE
);

CREATE TABLE apartment_images (
    ImageID INT AUTO_INCREMENT PRIMARY KEY,
    ApartmentID INT,
    ImageURL VARCHAR(255),
    FOREIGN KEY (ApartmentID) REFERENCES apartments(ApartmentId)
);

