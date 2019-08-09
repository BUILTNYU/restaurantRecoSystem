-- Create a database called UrbanConnector

-- three schemas in total 

-- one for storing all recommendations for all users, including user_id, restaurant_id, context information, timestamp

CREATE TABLE IF NOT EXISTS `AllRecommendations`(
    `user_id` VARCHAR(30), 
    `restaurant_id` VARCHAR(30),
    `recommendation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `context` JSON,
    `local_time` VARCHAR(30),
    PRIMARY KEY (`user_id`, `restaurant_id`, `recommendation_time`)
);

-- one for storing recommendations made only in the past 7 days
CREATE TABLE IF NOT EXISTS `RecommendationsSevenDays`(
    `user_id` VARCHAR(30), 
    `restaurant_id` VARCHAR(30), 
    `recommendation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP , 
    FOREIGN KEY (user_id, restaurant_id, recommendation_time) REFERENCES AllRecommendations(user_id, restaurant_id, recommendation_time) ON DELETE CASCADE
);

-- one for storing user rating 
CREATE TABLE IF NOT EXISTS `UserRating`(
    `user_id` VARCHAR(30), 
    `restaurant_id` VARCHAR(30), 
    `recommendation_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP , 
    `user_selection_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `reward` FLOAT,
    FOREIGN KEY (user_id, restaurant_id, recommendation_time) REFERENCES AllRecommendations(user_id, restaurant_id, recommendation_time) ON DELETE CASCADE
);
