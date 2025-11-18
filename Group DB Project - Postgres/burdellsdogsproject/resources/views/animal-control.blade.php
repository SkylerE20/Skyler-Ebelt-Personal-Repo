<!DOCTYPE html>
<html>
<head>
    <title>Animal Control Report</title>
</head>
<style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
    }
</style>
<body>
    <h1>Animal Control Report</h1>
    
    <table>
        <tr>
            <th>Month</th>
            <th>Animal Control Surrenders</th>
            <th>Dogs Adopted (60+ days)</th>
            <th>Total Expenses</th>
        </tr>
        
        @foreach($months as $monthData)
        <tr>
            <td>{{ $monthData['month_label'] }}</td>
            <td>
                <a href="{{ url('/reports/drill-down/surrendered/' . $monthData['start_date'] . '/' . $monthData['end_date']) }}">
                    {{ $monthData['ac_surrendered'] }}
                </a>
            </td>
            <td>
                <a href="{{ url('/reports/drill-down/60plus/' . $monthData['start_date'] . '/' . $monthData['end_date']) }}">
                    {{ $monthData['60plus'] }}
                </a>
            </td>
            <td>
                <a href="{{ url('/reports/drill-down/expenses/' . $monthData['start_date'] . '/' . $monthData['end_date']) }}">
                    ${{ number_format($monthData['total_expenses'], 2) }}
                </a>
            </td>
        </tr>
        @endforeach
    </table>
    
    <a href="{{ url('/dogdashboard') }}" class="back-link">Back to Dashboard</a>
</body>
</html>