-- Create an index named 'idx_name_first' on the 'names' table.
-- This index will be created on the first letter of the 'name' column.
CREATE INDEX idx_name_first ON names (name (1));
