SELECT
    id,
    operation_type,
    status,
    created_at,
    input_files,
    output_files,
    error_message
FROM operation_history
ORDER BY created_at DESC;