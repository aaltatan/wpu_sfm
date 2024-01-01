queries = {
    'default': """SELECT 
                    receipts.id,
                    receipts.created_at,
                    receipts.date,
                    receipts.client_id,
                    receipts.client,
                    receipts.notes,
                    receipts.is_closed,
                    faculties.title,
                    users.fullname,
                    SUM(receipts_details.price * receipts_details.quantity) AS total_price
                FROM 
                    receipts
                LEFT JOIN users ON receipts.user_id = users.id
                LEFT JOIN faculties ON receipts.faculty_id = faculties.id
                LEFT JOIN receipts_details ON receipts.id = receipts_details.receipt_id
                WHERE users.id = :user_id
                GROUP BY
                    receipts.id,
                    receipts.created_at,
                    receipts.date,
                    receipts.client_id,
                    receipts.client,
                    receipts.notes,
                    faculties.title,
                    users.fullname
                ORDER BY
                    receipts.date DESC;"""
}
