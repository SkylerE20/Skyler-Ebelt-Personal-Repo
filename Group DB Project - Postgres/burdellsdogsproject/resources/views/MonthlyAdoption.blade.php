<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Burdell's Dogs - Monthly Adoption Report</title>
</head>
<style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
    }
</style>
<body>

<h2>Monthly Adoption Report</h2>

@if(isset($monthlyAdoptionTable) && count($monthlyAdoptionTable) > 0)
<table>
    <tr>
        <th>Month</th>
        <th>Breed</th>
        <th># Adopted</th>
        <th># Surrendered</th>
        <th>Total Expenses ($)</th>
        <th>Total Adoption Fees ($)</th>
        <th>Net Profit ($)</th>
    </tr>
    @foreach($monthlyAdoptionTable as $row)
    <tr>
        <td>{{ $row->monthcol }}</td>
        <td>{{ $row->breed }}</td>
        <td>{{ $row->adopted_count }}</td>
        <td>{{ $row->surrendered_count }}</td>
        <td>${{ number_format($row->total_expenses, 2) }}</td>
        <td>${{ number_format($row->total_fees, 2) }}</td>
        <td>${{ number_format($row->net_profit, 2) }}</td>
    </tr>
    @endforeach
</table>
@else
<p>No adoption data available.</p>
@endif

</body>
</html>
