import pandas as pd

# Dummy data matching the required format
data = {
    'InvoiceNo': ['INV-1001', 'INV-1002', 'INV-1003'],
    'Date': ['2026-09-24', '2026-09-25', '2026-09-26'],
    'CustomerName': ['Rahim Ahmed', 'Karim Chowdhury', 'John Doe'],
    'CustomerEmail': ['rahim@example.com', 'karim@example.com', 'john@example.com'],
    'ItemDescription': ['Nike Air Max', 'Adidas Ultraboost', 'Puma RS-X'],
    'Quantity': [1, 2, 1],
    'UnitPrice': [120.00, 150.00, 90.00],
    'TotalAmount': [120.00, 300.00, 90.00]
}

# Create DataFrame and export to Excel
df = pd.DataFrame(data)
df.to_excel('sample_orders.xlsx', index=False)

print("Sample Excel file 'sample_orders.xlsx' created successfully!")