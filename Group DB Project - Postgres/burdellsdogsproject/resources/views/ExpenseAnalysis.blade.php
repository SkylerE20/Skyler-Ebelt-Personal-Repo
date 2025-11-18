<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Burdell's Dogs - Expense Analysis Report</title>
</head>
<style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
    }
</style>
<body>

<h2>Expense Analysis Report</h2>

@if(isset($expenseAnalysisTable) && count($expenseAnalysisTable) > 0)
<table>
    <tr>
        <th>Vendor</th>
        <th>Total Expense ($)</th>
    </tr>
    @foreach($expenseAnalysisTable as $row)
    <tr>
        <td>{{ $row->vendor }}</td>
        <td>${{ number_format($row->total_expense, 2) }}</td>
    </tr>
    @endforeach
</table>

@else
<p>No expense data available.</p>
@endif

</body>
</html>
