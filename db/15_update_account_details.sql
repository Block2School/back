ALTER TABLE account_details
ADD COLUMN private enum('public', 'private', 'friends') DEFAULT 'public';