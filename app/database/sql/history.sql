INSERT INTO operation_history (
    operation_type,
    status,
    created_at,
    input_files,
    output_files,
    error_message
)
VALUES (?, ?, ?, ?, ?, ?);