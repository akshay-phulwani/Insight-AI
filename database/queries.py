from database.connection import get_connection


def dataset_exists(file_name, total_rows, total_columns):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM Datasets
    WHERE file_name = ?
    AND total_rows = ?
    AND total_columns = ?
    """

    cursor.execute(query, (file_name, total_rows, total_columns))
    exists = cursor.fetchone()[0] > 0

    conn.close()

    return exists


def insert_dataset(file_name, file_type, total_rows, total_columns):

    if dataset_exists(file_name, total_rows, total_columns):
        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Datasets
    (file_name, file_type, total_rows, total_columns)
    VALUES (?, ?, ?, ?)
    """

    cursor.execute(
        query,
        (
            file_name,
            file_type,
            total_rows,
            total_columns
        )
    )

    conn.commit()
    conn.close()
